from pathlib import Path
import sys,json,shutil
sys.path.insert(0,str(Path('.tools/font-subset').resolve()))
from PIL import Image
from fontTools import subset
p=Path('.')
source=p/'assets-source';source.mkdir(exist_ok=True)
(source/'images').mkdir(exist_ok=True)
(source/'fonts').mkdir(exist_ok=True)
for f in (p/'public/images').glob('*.png'):
 Image.open(f).convert('RGB').save(f.with_suffix('.webp'),quality=84,method=6)
 f.rename(source/'images'/f.name)
content=p/'content/archives.json'
c=json.loads(content.read_text(encoding='utf-8'))
for r in c['records']:r['image']=r['image'].replace('.png','.webp')
content.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
chars=set(chr(i) for i in range(32,127))
for root in [p/'src',p/'content']:
 for f in root.rglob('*'):
  if f.is_file():
   try:chars.update(f.read_text(encoding='utf-8'))
   except UnicodeError:pass
for f in (p/'public/fonts').glob('*.woff2'):
 original=source/'fonts'/f.name
 f.rename(original)
 options=subset.Options();options.flavor='woff2';options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
 font=subset.load_font(str(original),options)
 sub=subset.Subsetter(options=options);sub.populate(text=''.join(chars));sub.subset(font)
 subset.save_font(font,str(f),options)
 print(f.name,original.stat().st_size,'->',f.stat().st_size)
f=p/'content/替换指南.md';s=f.read_text(encoding='utf-8').replace('六张 AI 生成占位图在 public/images。','六张 AI 生成占位图的网页 WebP 版在 public/images，PNG 原图保存在 assets-source/images。').replace('推荐横向 16:9。','推荐横向 16:9。支持 JPG、PNG、WebP；替换时同步修改 image 路径。');s+='\n字体为当前内容的 MiSans 子集，未收录的新增字形使用系统中文字体回退。原完整字体与原始图片保留在 assets-source，需要时可重新生成子集或恢复完整字体。\n';f.write_text(s,encoding='utf-8')
f=p/'verification/PORTFOLIO.md';s=f.read_text(encoding='utf-8').replace('six generated PNGs copied to public/images','six generated PNGs retained in assets-source/images; visually identical composition encoded to public/images/*.webp');s+='\n- Distribution optimization: original font binaries preserved in assets-source/fonts, published fonts subset to source/content characters plus ASCII. Full glyph fallback uses system fonts.\n';f.write_text(s,encoding='utf-8')
print('Original assets preserved; web assets optimized.')
