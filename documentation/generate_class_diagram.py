from umlfy.class_diagram import generate_class_diagram

app_path = r'C:\Users\ashik\OneDrive\Desktop\projects\phonebook2\phonebook_2'
package_names = ["database", "fastapi", "features", "requests"]
output_file = r'C:\Users\ashik\OneDrive\Desktop\projects\phonebook2\phonebook_2\documentation\diagram.puml'

generate_class_diagram(app_path, package_names, output_file)
