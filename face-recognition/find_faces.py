import face_recognition

image = face_recognition.load_image_file("images/images.jpeg")
face_locations = face_recognition.face_locations(image)

print(face_locations)
print("There are",{len(face_locations)})