from PIL import Image
# Загружаем изображение
image = Image.open("new1.png")
pixels = image.load()

# Извлекаем синий канал и собираем байты
text_bytes = []
for y in range(image.height):
    for x in range(image.width):
        r, g, b = pixels[x, y]  # Получаем значения RGB
        text_bytes.append(b)  # Берём только синий канал

# Преобразуем байты в текст
text = bytes(text_bytes).decode("utf-8", errors="ignore")
print(text)
