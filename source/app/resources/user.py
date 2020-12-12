from werkzeug.security import generate_password_hash, check_password_hash

from flask import redirect, render_template, request, url_for, abort
from flask_login import login_user, login_required, current_user
from app.helpers.forms.signup_form import SignupForm
from app.helpers.forms.user_seeker_form import UserSeekerForm
from app.helpers.forms.update_user_form import UpdateUserForm
from app.helpers.permission import permission
from app.helpers.alert import add_alert, get_alert
from app.models.user import User
from app.models.alert import Alert
from app.models.configuration import Configuration


@login_required
def profile():
    return render_template("user/profile.html", user=current_user)



@permission('user_index')
def index():

    search_form = UserSeekerForm(request.args)

    users = User.search(search_query=search_form.search_query.data,
                        user_state=search_form.user_state.data,
                        page=int(request.args.get('page', 1)),
                        per_page=Configuration.query.first().items_per_page)

    return render_template("user/index.html", users=users, search_form=search_form, alert=get_alert())

@permission('user_create')
def new():
    return render_template("user/new.html", form=SignupForm())

@permission('user_create')
def create():
    form = SignupForm(id=None)

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    name=form.name.data, surname=form.surname.data,
                    password=generate_password_hash(form.password.data),
                    roles=form.roles.data)
        user.save()
        add_alert(
            Alert("success", f"El usuario {user.username} se creo correctamente."))
        return redirect(url_for("user_index"))

    return render_template("user/new.html", form=form)


@ permission('user_update')
def edit(id):
    user = User.query.get(id)

    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    return render_template("user/edit.html", user_id=id, is_admin=user.has_role("Administrador"), update_form=UpdateUserForm(obj=user))

@ permission('user_update')
def update(id):
    update_form = UpdateUserForm(id=id)

    if not update_form.validate_on_submit():
        return render_template("user/edit.html", user_id=id, update_form=update_form)

    user = User.update(id, update_form.name.data, update_form.surname.data,
                       update_form.email.data, update_form.username.data, update_form.roles.data, update_form.is_active.data, update_form.password.data)

    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    add_alert(
        Alert("success", f"El usuario {user.username} se actualizo correctamente."))

    return redirect(url_for("user_index"))

@ permission('user_delete')
def delete(id):
    user = User.delete(id)
    if user:
        add_alert(
            Alert("success", f"El usuario {user.username} se borro con exito."))
    else:
        add_alert(Alert("danger", "El usuario no existe."))

    return redirect(url_for("user_index"))
