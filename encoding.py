from chardet.universaldetector import UniversalDetector
detector = UniversalDetector()
with open('Template_for_import_or_modify (3)_BSS_4G_E_27122024.csv', 'rb') as fh:
    for line in fh:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(detector.result)