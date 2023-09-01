# Импорт Aspose.Words для модуля Python
import aspose.words as aw

# загрузить файл PDF и преобразовать в формат Word DOCX
pdf = aw.Document("222.pdf")
pdf.save("pdf.docx")

# загрузить версию PDF в формате DOCX
doc = aw.Document("pdf.docx")

# получить все формы
shapes = doc.get_child_nodes(aw.NodeType.SHAPE, True)
imageIndex = 0

# цикл по фигурам
for shape in shapes :
    shape = shape.as_shape()
    if (shape.has_image) :

        # установить имя файла изображения
        imageFileName = f"Image.ExportImages.{imageIndex}_{aw.FileFormatUtil.image_type_to_extension(shape.image_data.image_type)}"

        # сохранить изображение
        shape.image_data.save(imageFileName)
        imageIndex += 1