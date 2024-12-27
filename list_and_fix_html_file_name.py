import os

html_files = [f for f in os.listdir('./contents') if f.endswith('.html')]

for filename in html_files:
    new_filename = filename.replace(' ', '_')
    old_path = os.path.join('./contents', filename)
    new_path = os.path.join('./contents', new_filename)
    os.rename(old_path, new_path)

html_files = [f for f in os.listdir('./contents') if f.endswith('.html')]

index = 0
print("\nRenamed HTML files:")
while index < len(html_files):
    print(html_files[index])
    index += 1
