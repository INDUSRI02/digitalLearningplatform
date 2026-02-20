import polib

def fix_po_newlines(file_path):
    po = polib.pofile(file_path)
    for entry in po:
        if entry.msgid.startswith('\n') and not entry.msgstr.startswith('\n'):
            entry.msgstr = '\n' + entry.msgstr
        if entry.msgid.endswith('\n') and not entry.msgstr.endswith('\n'):
            entry.msgstr = entry.msgstr + '\n'
    po.save()

fix_po_newlines('locale/hi/LC_MESSAGES/django.po')
fix_po_newlines('locale/te/LC_MESSAGES/django.po')
print("Newlines fixed! Now manually check the variable placeholders in the lines reported.")