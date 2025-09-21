import os
import piexif
from PIL import Image, ImageDraw, ImageFont

def get_exif_date(img_path):
    try:
        exif_dict = piexif.load(img_path)
        date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
        return date_str.split(' ')[0].replace(':', '-')
    except Exception:
        return None

def add_watermark(img_path, text, font_size, color, position, out_dir):
    image = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w, h = image.size

    if position == 'left_top':
        pos = (10, 10)
    elif position == 'center':
        pos = ((w - text_w) // 2, (h - text_h) // 2)
    elif position == 'right_bottom':
        pos = (w - text_w - 10, h - text_h - 10)
    else:
        pos = (10, 10)

    draw.text(pos, text, fill=color, font=font)
    base_name = os.path.basename(img_path)
    out_path = os.path.join(out_dir, base_name)
    exif_bytes = image.info.get("exif")
    if exif_bytes:
        image.save(out_path, exif=exif_bytes)
    else:
        image.save(out_path)
    print(f"水印图片已保存为: {out_path}")

def main():
    dir_path = input("请输入图片文件夹路径: ").strip()
    if not os.path.isdir(dir_path):
        print("文件夹不存在！")
        return

    font_size = int(input("请输入字体大小(如32): ").strip())
    color = input("请输入字体颜色(如red或#FF0000): ").strip()
    position = input("请输入水印位置(left_top/center/right_bottom): ").strip()

    out_dir = os.path.join(dir_path, os.path.basename(dir_path) + "_watermark")
    os.makedirs(out_dir, exist_ok=True)

    exts = ('.jpg', '.jpeg', '.png')
    files = [f for f in os.listdir(dir_path) if f.lower().endswith(exts)]
    if not files:
        print("未找到图片文件。")
        return

    for fname in files:
        img_path = os.path.join(dir_path, fname)
        date = get_exif_date(img_path)
        if not date:
            print(f"{fname} 未找到拍摄时间，跳过。")
            continue
        add_watermark(img_path, date, font_size, color, position, out_dir)

if __name__ == "__main__":
    main()
