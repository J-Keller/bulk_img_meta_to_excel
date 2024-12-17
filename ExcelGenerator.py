import dearpygui.dearpygui as dpg
import bulk_img_meta_to_excel as app


dpg.create_context()

def callback(sender, app_data):
    dpg.set_value(sender, app_data['file_path_name'])

def cancel_callback(sender, app_data):
    print("File dialog canceled")

def submit_action(sender, app_data, user_data):
    input_folder = dpg.get_value("input_folder")
    output_folder = dpg.get_value("output_folder")

    # Replace this with your processing logic
    print(f"Input Folder: {input_folder}\nOutput Folder: {output_folder}\nProcessing started!")
    app.export_excel(input_folder, output_folder)

def setup_ui():
    with dpg.window(label="Folder Selector", no_title_bar=True, width=900, height=600):
        dpg.add_text("Select folders for input and output below:")

        dpg.add_input_text(label="Input Folder", tag="input_folder", readonly=True, width=300)
        dpg.add_button(label="Browse Input", callback=lambda: dpg.show_item("input_file_dialog"))

        dpg.add_spacing(count=2)

        dpg.add_input_text(label="Output Folder", tag="output_folder", readonly=True, width=300)
        dpg.add_button(label="Browse Output", callback=lambda: dpg.show_item("output_file_dialog"))

        dpg.add_spacing(count=2)

        dpg.add_button(label="Submit", callback=submit_action, width=200)

    # Input file dialog
    with dpg.file_dialog(directory_selector=True, show=False, callback=lambda s, a, u: dpg.set_value("input_folder", a["file_path_name"]), tag="input_file_dialog", cancel_callback=cancel_callback, width=600, height=400):
        dpg.add_file_extension(".*")

    # Output file dialog
    with dpg.file_dialog(directory_selector=True, show=False, callback=lambda s, a, u: dpg.set_value("output_folder", a["file_path_name"]), tag="output_file_dialog", cancel_callback=cancel_callback, width=600, height=400):
        dpg.add_file_extension(".*")

# Run the application

setup_ui()
dpg.create_viewport(title='Folder Selector', width=900, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
