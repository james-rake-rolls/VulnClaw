# Social-Engineering Intel Aggregation

## Persona-Profiling Framework

### Information Dimensions

| Dimension | Data source | Extraction method |
|------|--------|---------|
| Identity marker | Page meta, GitHub | Regex-extract author/copyright |
| Social networks | External page links | `<a href>` matching social-media domains |
| Tech preference | GitHub repo language distribution | GitHub API |
| Geolocation | GitHub location, blog | Profile page |
| Occupation info | GitHub company, LinkedIn | Profile page |
| Contact info | GitHub email, blog contact page | API + page extraction |
| Interests | GitHub repo topics, blog posts | Repo topics + article categories |

## Cross-Verification

### Principles
1. **Do not trust a single source** — key info needs at least 2 independent sources
2. **Timeliness labeling** — note when info was obtained; flag stale info separately
3. **Confidence rating**:
   - 🟢 **High**: confirmed by multiple independent sources
   - 🟡 **Medium**: a single reliable source
   - 🔴 **Low**: inferred / unverified

### Common Correlation Patterns

```
blog GitHub link -> GitHub username -> GitHub API for the email
                                  -> GitHub API fetches repos -> infer the tech stack
                                  -> GitHub commit email -> correlate other identities

blog Bilibili link -> Bilibili UID -> Bilibili profile -> following/followers -> interest tags
                                    -> uploaded videos -> technical field

username -> cross-platform search -> discover more social accounts
email -> haveibeenpwned -> data-breach records
```

## Social-Media Information Extraction

### Bilibili
```python
import re

def extract_bilibili_uid(url):
    """Extract the UID from a Bilibili URL"""
    # space.bilibili.com/12345
    m = re.search(r'bilibili\.com/(\d+)', url)
    if m:
        return m.group(1)
    return None
```

### Weibo
```python
def extract_weibo_uid(url):
    """Extract the UID from a Weibo URL"""
    # weibo.com/u/12345 or weibo.com/username
    m = re.search(r'weibo\.com/(?:u/)?(\w+)', url)
    if m:
        return m.group(1)
    return None
```

### Zhihu
```python
def extract_zhihu_username(url):
    """Extract the username from a Zhihu URL"""
    # zhihu.com/people/username
    m = re.search(r'zhihu\.com/people/([^/?]+)', url)
    if m:
        return m.group(1)
    return None
```

## Intel-Aggregation Report Format

```markdown
# Target Recon Report

## 📋 Basic Info
| Item | Content | Confidence | Source |
|------|------|--------|------|
| Target | https://xxx | - | User input |
| Framework | Hexo | 🟢 | HTTP header + HTML traits |
| Server | GitHub Pages | 🟢 | Server header |
| Author | XXX | 🟢 | meta author |
| ... | ... | ... | ... |

## 👤 Persona
- **Nickname**: XXX
- **GitHub**：https://github.com/xxx
- **Bilibili**: https://space.bilibili.com/xxx
- **Tech stack**: Python / JavaScript
- **Location**: Shenzhen
- ...

## 🔗 Correlated Findings
- [finding 1]
- [finding 2]

## 📌 Key Findings
1. ...
2. ...

---
*Report generated: YYYY-MM-DD HH:MM*
*Data sources: the target site, the GitHub API, public social-media info*
```

## Privacy and Ethics

- ✅ Collect only **public information** (content reachable without logging in)
- ✅ Do not try to log into others' accounts
- ✅ Do not use collected info for harassment or social-engineering attacks
- ✅ Cite the source of information to keep it traceable
- ❌ Do not collect private communications
- ❌ Do not use information for phishing or other deception
