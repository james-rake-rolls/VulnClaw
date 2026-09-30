# Author-Tracking Methods

## Core Workflow

```
extract the author marker from the page -> determine a unique identifier (username/email) -> cross-platform search -> aggregate
```

## Step 1: Extract the Author Identifier from the Page

### HTML Meta Tags
```python
import re

def extract_author_from_meta(html):
    """Extract author info from HTML meta tags"""
    authors = []
    
    # <meta name="author" content="XXX">
    m = re.findall(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', html)
    authors.extend(m)
    
    # <meta name="copyright" content="XXX">
    m = re.findall(r'<meta\s+name=["\']copyright["\']\s+content=["\']([^"\']+)["\']', html)
    authors.extend(m)
    
    # OG tags
    m = re.findall(r'<meta\s+property=["\']article:author["\']\s+content=["\']([^"\']+)["\']', html)
    authors.extend(m)
    
    return list(set(authors))
```

### Page-Link Extraction
```python
def extract_social_links(html):
    """Extract social-media links from a page"""
    links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
    
    social = {}
    for link in links:
        if 'github.com' in link:
            social['github'] = link
        elif 'bilibili.com' in link:
            social['bilibili'] = link
        elif 'weibo.com' in link or 'weibo.cn' in link:
            social['weibo'] = link
        elif 'zhihu.com' in link:
            social['zhihu'] = link
        elif 'twitter.com' in link or 'x.com' in link:
            social['twitter'] = link
        elif 'linkedin.com' in link:
            social['linkedin'] = link
        elif 'youtube.com' in link:
            social['youtube'] = link
        elif 'facebook.com' in link:
            social['facebook'] = link
    
    return social
```

## Step 2: GitHub Tracking

### User-Info API
```python
import requests

def get_github_profile(username):
    """Fetch a GitHub user's public info"""
    r = requests.get(f"https://api.github.com/users/{username}")
    if r.status_code != 200:
        return None
    
    data = r.json()
    return {
        'name': data.get('name'),
        'bio': data.get('bio'),
        'email': data.get('email'),
        'blog': data.get('blog'),
        'location': data.get('location'),
        'company': data.get('company'),
        'public_repos': data.get('public_repos'),
        'followers': data.get('followers'),
        'following': data.get('following'),
        'created_at': data.get('created_at'),
        'avatar_url': data.get('avatar_url'),
    }

def get_github_repos(username):
    """Fetch a user's public repos (infer the tech stack)"""
    r = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100")
    if r.status_code != 200:
        return []
    
    repos = r.json()
    languages = {}
    for repo in repos:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    return {
        'top_languages': sorted(languages.items(), key=lambda x: -x[1])[:5],
        'repo_count': len(repos),
        'starred_total': sum(r.get('stargazers_count', 0) for r in repos),
    }
```

### Extract Email from GitHub Commits
```python
def get_github_commit_email(username, repo):
    """Extract the author's email from GitHub commits"""
    r = requests.get(f"https://api.github.com/repos/{username}/{repo}/commits?per_page=10")
    if r.status_code != 200:
        return []
    
    emails = set()
    for commit in r.json():
        author = commit.get('commit', {}).get('author', {})
        if author.get('email'):
            emails.add(author['email'])
    
    return list(emails)
```

## Step 3: Cross-Platform Correlation

### Search Other Platforms by Username
```python
# Common-platform detection
PLATFORMS = {
    'GitHub': 'https://github.com/{username}',
    'Bilibili': 'https://space.bilibili.com/search?keyword={username}',
    'Zhihu': 'https://www.zhihu.com/search?type=content&q={username}',
    'CSDN': 'https://blog.csdn.net/{username}',
    'Juejin': 'https://juejin.cn/user/{username}',
    'Twitter': 'https://twitter.com/{username}',
    'LinkedIn': 'https://www.linkedin.com/in/{username}',
}

async def cross_platform_search(username, fetch_tool):
    """Search multiple platforms by username"""
    results = {}
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)
        try:
            resp = await fetch_tool(url=url)
            if resp.get('status') == 200:
                results[platform] = f"✅ found ({url})"
            else:
                results[platform] = f"❌ not found"
        except:
            results[platform] = f"⚠️ detection failed"
    return results
```

## Step 4: Information-Aggregation Template

```markdown
## Persona: {nickname}

### Basic Info
- **Nickname**: xxx
- **Real name**: xxx (if any)
- **Email**: xxx
- **Location**: xxx
- **Occupation/company**: xxx

### Technical Profile
- **Primary language**: Python / JavaScript / ...
- **Tech-stack preference**: ...
- **Open-source contributions**: N repos, M stars
- **Areas of interest**: ...

### Social Media
- GitHub: xxx
- Bilibili: xxx
- Zhihu: xxx
- ...

### Correlated Information
- Same ID across platforms: xxx
- Known projects: xxx
- Historical leaks: xxx
```
