from PIL import Image

def compare_png_pixels(file1, file2):
    try:
        # 打开两个 PNG 文件
        img1 = Image.open(file1)
        img2 = Image.open(file2)

        # 确保两个图像的尺寸相同
        if img1.size != img2.size:
            print("两个图像的尺寸不同，无法直接比较像素。")
            return

        width, height = img1.size
        total_pixels = width * height
        different_pixels = 0
        different_positions = []

        # 遍历每个像素并比较
        for x in range(width):
            for y in range(height):
                pixel1 = img1.getpixel((x, y))
                pixel2 = img2.getpixel((x, y))
                if pixel1 != pixel2:
                    different_pixels += 1
                    different_positions.append((x, y))

        # 计算差异百分比
        difference_percentage = (different_pixels / total_pixels) * 100

        print(f"总像素数: {total_pixels}")
        print(f"不同像素数: {different_pixels}")
        print(f"像素差异百分比: {difference_percentage:.2f}%")
        if different_positions:
            print("不一样的点的位置：")
            for position in different_positions:
                print(f"({position[0]}, {position[1]})")
        else:
            print("两个图像的像素完全相同。")

    except Exception as e:
        print(f"发生错误: {e}")

    









in0 = "/home/yy/my_script/tinyrenderer_learn/lesson3/190.png"
in1 = "/home/yy/my_script/tinyrenderer_learn/lesson3/191.png"

compare_png_pixels(in0, in1)
