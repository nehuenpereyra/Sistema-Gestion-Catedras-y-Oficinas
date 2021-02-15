import re
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import User, Role, MailSender
from app.helpers.forms import UserCreateForm, UserUpdateForm, PasswordRecoveryForm, PasswordChangeForm, UserSeeker


@permission('user_index')
def index():
    allowed_user_ids = None

    if not current_user.is_admin():
        allowed_user_ids = current_user.allowed_user_id_list()

    form = UserSeeker(request.args)
    args = {
        "user_attributes": form.user_attributes.data,
        "user_rol_ids": form.user_rol.data,
        "search_text": form.search_text.data if form.search_text.data != "" else None,
        "page": int(request.args.get('page', 1)),
        "per_page": Configuration.query.first().items_per_page
    }
    users = User.search(**args)

    return render_template("user/index.html", users=users, alert=get_alert(), form=form)


@ permission('user_show')
def show(id):
    user = User.get(id)
    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    return render_template("user/show.html", user=user, alert=get_alert())


@ permission('user_create')
def new():
    return render_template("user/new.html", form=UserCreateForm())


@ permission('user_create')
def create():
    form = UserCreateForm(id=None)
    if form.validate_on_submit():
        user = User(name=form.name.data, surname=form.surname.data, username=form.username.data, password=form.password.data,
                    institutional_email=form.institutional_email.data, secondary_email=form.secondary_email.data)
        user.set_roles(Role.get_all(form.roles.data))
        user.save()
        add_alert(
            Alert("success", f'El usuario "{user.name} {user.surname}" se ha creado correctamente.'))
        recovery_link = user.set_recovery_link()
        string_link = "{}/user/password_change/{}".format(re.match("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", request.base_url).group(),
                                                          recovery_link)
        # MailSender.send_to_user("Contraseña para acceder al sistema de cátedras y oficinas de la facultad de ciencias médicas",
        #                        f"Acceda al siguiente enlace para establecer la contraseña: {string_link}",
        #                        user.institutional_email)
        return redirect(url_for("user_index"))
    return render_template("user/new.html", form=form)


@permission('user_update')
def edit(id):
    user = User.get(id)
    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    form = UserUpdateForm(obj=user)
    form.roles.data = user.roles.collect(lambda each: each.id)

    return render_template("user/edit.html", user=user, form=form)


@permission('user_update')
def update(id):
    user = User.get(id)

    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    form = UserUpdateForm(id=id)
    if not form.validate_on_submit():
        return render_template("user/edit.html", user=user, form=form)

    user.update(name=form.name.data, surname=form.surname.data, username=form.username.data, password=form.password.data,
                institutional_email=form.institutional_email.data, secondary_email=form.secondary_email.data, roles=Role.get_all(form.roles.data))

    add_alert(
        Alert("success", f'El usuario "{user.name} {user.surname}" se ha modificado correctamente.'))

    return redirect(url_for("user_index"))


@permission('user_delete')
def delete(id):
    user = User.get(id)
    if not user or user.is_deleted:
        add_alert(Alert("danger", "El usuario no existe."))
    else:
        user.remove()
        add_alert(
            Alert("success", f'El usuario "{user.name} {user.surname}" se ha borrado correctamente.'))
    return redirect(url_for("user_index"))


def password_recovery():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        form = PasswordRecoveryForm(id=None)
        if form.validate_on_submit():
            user = User.find_by_institutional_email(
                form.user_email.data)
            if not user.is_empty():
                user = user.first()
                recovery_link = user.set_recovery_link()
                string_link = "{}/user/password_change/{}".format(re.match("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", request.base_url).group(),
                                                                  recovery_link)
                try:
                    MailSender.send_to_user("Correo de recuperación de contraseña",
                                            f"Acceda al siguiente enlace para cambiar su contraseña: {string_link}",
                                            user.institutional_email)
                except Exception as e:
                    add_alert(
                        Alert("danger", "Ha ocurrido un error al enviar el correo."))
                    return redirect(url_for('user_password_recovery'))
                add_alert(
                    Alert("success", f'Se envio un correo al email institucional.'))
            else:
                add_alert(
                    Alert("danger", "No existe usuario con ese email institucional."))
        return redirect(url_for('user_password_recovery'))
    return render_template("user/password_recovery.html", alert=get_alert(), form=PasswordRecoveryForm())


def password_change(url_recovery):
    user = User.find_by_recovery_link(url_recovery)
    if not user or current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        form = PasswordChangeForm(id=None)
        if form.validate_on_submit():
            print(form.user_password.data)
            user.set_password(form.user_password.data)
            user.remove_recovery_link()
            add_alert(
                Alert("success", 'Se cambió la contraseña correctamente.'))
            return redirect(url_for('auth_login'))
    return render_template("user/password_change.html", url_recovery=url_recovery, form=PasswordChangeForm())


@ permission('user_show')
def password_change_authenticated():
    form = PasswordChangeForm()
    form.submit.label.text = "Guardar"
    if request.method == 'POST':
        form = PasswordChangeForm(id=None)
        if form.validate_on_submit():
            current_user.set_password(form.user_password.data)
            current_user.save()
            add_alert(
                Alert("success", 'Se cambió la contraseña correctamente.'))
            return redirect(url_for('user_show', id=current_user.id))
    return render_template("user/password_change_authenticated.html", form=form)
