from flask_ckeditor import CKEditor

ckeditor = CKEditor()

def set_CKEditor(app):
    ckeditor.init_app(app)