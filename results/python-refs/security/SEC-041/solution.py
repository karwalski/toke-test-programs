import sys
import base64
import binascii

def analyze_java_serialization(data):
    try:
        # Convert hex to bytes
        binary_data = binascii.unhexlify(data)
        
        # Check for Java serialization magic bytes
        if binary_data.startswith(b'\xac\xed'):
            return "Java serialisation magic bytes"
        
        # Check for common dangerous classes
        dangerous_patterns = [
            b'java.lang.Runtime',
            b'java.lang.ProcessBuilder',
            b'sun.reflect.annotation.AnnotationInvocationHandler',
            b'org.apache.commons.collections.functors.InvokerTransformer',
            b'org.apache.commons.collections.functors.ChainedTransformer',
            b'com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in binary_data:
                return "DANGEROUS"
        
        return "SAFE"
    except:
        return "SAFE"

def analyze_pickle(data):
    try:
        # Convert hex/base64 to bytes
        try:
            binary_data = binascii.unhexlify(data)
        except:
            binary_data = base64.b64decode(data)
        
        # Check for pickle magic bytes
        if binary_data.startswith(b'\x80'):
            # Pickle protocol 2+
            pass
        
        # Convert to string for pattern matching
        data_str = data.replace('\n', '')
        
        dangerous_patterns = [
            'c__builtin__\neval',
            'c__builtin__\nexec',
            'csubprocess\ncall',
            'csubprocess\nPopen',
            'cos\nsystem',
            'c__builtin__\n__import__',
            'cbuiltins\neval',
            'cbuiltins\nexec'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in data_str:
                return "DANGEROUS"
        
        return "SAFE"
    except:
        return "SAFE"

def analyze_php_serialization(data):
    try:
        dangerous_patterns = [
            'O:',  # Object serialization
            '__wakeup',
            '__destruct',
            '__toString',
            '__call',
            '__get',
            '__set',
            'eval',
            'system',
            'exec',
            'shell_exec',
            'file_get_contents',
            'file_put_contents'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in data:
                return "DANGEROUS"
        
        return "SAFE"
    except:
        return "SAFE"

def analyze_json(data):
    try:
        import json
        
        # Parse JSON
        parsed = json.loads(data)
        
        # Check for class hints that might indicate unsafe deserialization
        dangerous_patterns = [
            '__class__',
            '__module__',
            '__reduce__',
            '__reduce_ex__',
            '__getstate__',
            '__setstate__',
            'eval',
            'exec',
            'subprocess',
            '__import__'
        ]
        
        data_str = str(parsed).lower()
        for pattern in dangerous_patterns:
            if pattern in data_str:
                return "DANGEROUS"
        
        return "SAFE"
    except:
        return "SAFE"

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    format_type = lines[0]
    data = ''.join(lines[1:]) if len(lines) > 1 else ""
    
    if format_type == "java":
        result = analyze_java_serialization(data)
    elif format_type == "pickle":
        result = analyze_pickle(data)
    elif format_type == "php":
        result = analyze_php_serialization(data)
    elif format_type == "json":
        result = analyze_json(data)
    else:
        result = "SAFE"
    
    print(result)

if __name__ == "__main__":
    main()