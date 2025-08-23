# Bug Audit Report

Generated: 2025-08-23T16:38:30.201591

Total Bugs Found: **57**

## Summary

### By Source
- bandit: 57

### By Severity

### By Type
- security: 57

## Feature Impact

No bugs linked to specific features.

## Checklist Items Affected

### 2.1: Unknown Item
Related to 1 bugs:
- A FTP-related module is being imported.  FTP is considered insecure. Use SSH/SFTP/SCP or some other encrypted protocol.

### 2.2: Unknown Item
Related to 1 bugs:
- A FTP-related module is being imported.  FTP is considered insecure. Use SSH/SFTP/SCP or some other encrypted protocol.

### 3.1: Unknown Item
Related to 57 bugs:
- Possible binding to all interfaces.
- Using xml.etree.ElementTree to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.
- Using xml.dom.minidom.parseString to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.dom.minidom.parseString with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called
- Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
- Use of possibly insecure function - consider using safer ast.literal_eval.
- ... and 52 more

### 3.2: Unknown Item
Related to 57 bugs:
- Possible binding to all interfaces.
- Using xml.etree.ElementTree to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.
- Using xml.dom.minidom.parseString to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.dom.minidom.parseString with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called
- Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
- Use of possibly insecure function - consider using safer ast.literal_eval.
- ... and 52 more

### 6.1: Unknown Item
Related to 5 bugs:
- Using xml.etree.ElementTree to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.
- Using xml.dom.minidom.parseString to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.dom.minidom.parseString with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called
- Standard pseudo-random generators are not suitable for security/cryptographic purposes.
- Using pulldom to parse untrusted XML data is known to be vulnerable to XML attacks. Replace pulldom with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.
- Using xml.etree.ElementTree.parse to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree.parse with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called

### 6.2: Unknown Item
Related to 5 bugs:
- Using xml.etree.ElementTree to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.
- Using xml.dom.minidom.parseString to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.dom.minidom.parseString with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called
- Standard pseudo-random generators are not suitable for security/cryptographic purposes.
- Using pulldom to parse untrusted XML data is known to be vulnerable to XML attacks. Replace pulldom with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.
- Using xml.etree.ElementTree.parse to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree.parse with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called

## Detailed Bug List

