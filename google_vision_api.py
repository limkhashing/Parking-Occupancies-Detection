import io
import os
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_vision.json'


# [START vision_text_detection]
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    # [END vision_python_migration_text_detection]
# [END vision_text_detection]

detect_text("test_plate\\pic_009.jpg")
