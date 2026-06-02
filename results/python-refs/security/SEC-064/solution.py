import sys
import re
from urllib.parse import urlparse

def check_suspicious_tlds(domain):
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf', '.top', '.click', '.download']
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            return True
    return False

def check_url_shorteners(domain):
    shorteners = ['bit.ly', 'tinyurl.com', 'short.ly', 't.co', 'goo.gl', 'ow.ly', 'buff.ly']
    return domain in shorteners

def check_lookalike_domains(domain):
    # Common legitimate domains and their lookalikes
    legitimate_domains = {
        'paypal.com': ['paypa1.com', 'paypaI.com', 'payp4l.com', 'paipal.com'],
        'google.com': ['goog1e.com', 'googIe.com', 'g00gle.com'],
        'amazon.com': ['amaz0n.com', 'amazom.com', 'amazon.co'],
        'microsoft.com': ['microsft.com', 'microsooft.com', 'micr0soft.com'],
        'apple.com': ['app1e.com', 'appl3.com', 'aple.com'],
        'facebook.com': ['faceb00k.com', 'facebooke.com', 'face-book.com']
    }
    
    for legit_domain, lookalikes in legitimate_domains.items():
        if domain in lookalikes:
            return True
    return False

def check_malware_patterns(url):
    malware_patterns = [
        r'login.*secure.*update',
        r'verify.*account.*immediately',
        r'suspended.*click.*here',
        r'winner.*congratulations',
        r'urgent.*action.*required',
        r'phishing',
        r'malware',
        r'virus'
    ]
    
    url_lower = url.lower()
    for pattern in malware_patterns:
        if re.search(pattern, url_lower):
            return True
    return False

def analyze_url(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove www. prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        score = 0
        indicators = []
        
        # Check suspicious TLDs (20 points)
        if check_suspicious_tlds(domain):
            score += 20
            indicators.append('suspicious_tld')
        
        # Check URL shorteners (15 points)
        if check_url_shorteners(domain):
            score += 15
            indicators.append('url_shortener')
        
        # Check lookalike domains (40 points)
        if check_lookalike_domains(domain):
            score += 40
            indicators.append('lookalike_domain')
        
        # Check malware patterns (25 points)
        if check_malware_patterns(url):
            score += 25
            indicators.append('malware_pattern')
        
        # Additional checks
        
        # Check for suspicious characters in domain
        if re.search(r'[0-9]', domain.replace('.', '')):
            # Only add points if numbers replace letters suspiciously
            legit_with_numbers = ['1and1.com', '3m.com', '4chan.org']
            if domain not in legit_with_numbers and not domain.endswith('.co.uk'):
                score += 10
                indicators.append('suspicious_characters')
        
        # Check for excessive subdomains
        subdomain_count = domain.count('.')
        if subdomain_count > 3:
            score += 15
            indicators.append('excessive_subdomains')
        
        # Check for suspicious keywords in URL path
        suspicious_keywords = ['login', 'secure', 'verify', 'account', 'update', 'suspended']
        path_lower = parsed.path.lower()
        keyword_count = sum(1 for keyword in suspicious_keywords if keyword in path_lower)
        if keyword_count >= 2:
            score += 10
            indicators.append('suspicious_path')
        
        # Determine risk level
        if score >= 75:
            risk = 'critical'
        elif score >= 50:
            risk = 'high'
        elif score >= 25:
            risk = 'medium'
        else:
            risk = 'low'
        
        return {
            'url': url,
            'score': min(score, 100),
            'risk': risk,
            'indicators': indicators
        }
        
    except Exception:
        return {
            'url': url,
            'score': 0,
            'risk': 'low',
            'indicators': ['parse_error']
        }

def main():
    for line in sys.stdin:
        url = line.strip()
        if url:
            result = analyze_url(url)
            print(result['risk'])

if __name__ == '__main__':
    main()