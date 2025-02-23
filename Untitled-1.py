encoded_image = []
with open('\Graphs\generation\new\', "rb") as file:
        image_bytes = BytesIO(file.read())

        # Encode the image to a base64 string
        encoded_image.append(base64.b64encode(image_bytes.read()).decode("utf-8"))

with open('\Graphs\generation\used\', "rb") as file:
        image_bytes = BytesIO(file.read())

        # Encode the image to a base64 string
        encoded_image.append(base64.b64encode(image_bytes.read()).decode("utf-8"))