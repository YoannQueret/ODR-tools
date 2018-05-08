To use this mib with pysnmp, you need to install first pysnmp and pysmi :
- pip install pysnmp
- pip install pysmi

Move the MIB file to /usr/share/snmp/mibs/ with ext as .txt

As the user need to use the MIB with pysnmp run :
- mibdump.py ODR-DABMUX-MIB

Now you can find in your home directory ~/.pysnmp/mibs/ODR-DABMUX-MIB.py