# Android Signature Reverse Template

Use this template for Android sign, token, encrypt, decrypt, JNI, interceptor, and replay tasks.

## Template

```markdown
# Android Signature-Reversing Record

## Basic information

- APK / package name:
- Target feature:
- Target request:
- Target field:
- Current phase: static / dynamic / native / replay
- Current status: 🟡 in progress / ✅ closed out / ⛔ blocked
- Goal:
- Constraints:

## Static overview

| Item | Content |
| --- | --- |
| Manifest entry |  |
| Application |  |
| Main Activity / target component |  |
| Main package structure |  |
| Network framework |  |
| DI framework |  |
| Current conclusion |  |

## Request call flow

```text
Activity / Fragment / Service
-> ViewModel / Presenter / UseCase
-> Repository / DataSource
-> ApiService / RequestBuilder / Interceptor
-> Signer / Encryptor / Serializer
```

- Real call flow:
- Request Method / Path:
- Header write point:
- Body write point:
- Sign-input convergence point:
- Sequence / prerequisites:

## Sign / Crypto location

| Item | Content |
| --- | --- |
| Sign class / method |  |
| Encrypt class / method |  |
| Key constants |  |
| Key headers |  |
| Key Token / Device values |  |
| Java-only / Java+JNI / Native-first |  |

## Dynamic verification

| Hook point | Reason | Captured content | Result |
| --- | --- | --- | --- |
| Hook1 |  |  |  |

- URL:
- Headers:
- Body:
- Sign input:
- Sign output:
- Proxy verification:

## JNI / SO analysis

| Item | Content |
| --- | --- |
| Java native entry |  |
| SO name |  |
| JNI type | static / dynamic |
| Input parameters |  |
| Output role | final sign / intermediate token / other |
| Deeper RE needed? |  |

## Burp replay baseline

- Method:
- Path:
- Query:
- Headers:
- Body:
- Fields that must be kept:
- Fields that can be mutated:
- Preconditions:
- Needs device / hook / app assistance?:

## Conclusion

- Current closure level:
- Remaining blockers:
- Next-step recommendation:
```

## Minimum Required Fields

Even in a compact record, keep:

- APK or package
- target request
- real call-flow summary
- network stack
- sign or crypto location
- Java versus JNI conclusion
- one runtime hook or explicit reason why runtime is not needed
- Burp replay baseline or explicit blocker
