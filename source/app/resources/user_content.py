
from flask import redirect, render_template, request, url_for

from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import User, Career, Cathedra, Office, Configuration, Alert
from app.helpers.forms import CathedraSeeker, OfficeSeeker


@permission('user_content_index')
def index(user_id):

    user = User.get(user_id)

    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    if not user.is_responsible():
        add_alert(Alert("danger", "El usuario no es responsable de elementos."))
        return redirect(url_for("user_index"))

    page = int(request.args.get('page', 1))
    per_page = Configuration.get().items_per_page
    form = None

    kwargs = {
        "user": user,
        "alert": get_alert(),
        "workplace": ""
    }

    if user.is_career_manager():

        kwargs["messages"] = {
            "assigned": "Carrera Asignada",
            "to_assign": "Carreras Disponibles"
        }

        career = user.get_career()
        careers = [career] if career else []

        kwargs["workplace"] = "career"
        kwargs["assigned_elements"] = careers
        kwargs["elements_to_assign"] = Career.all_paginated(
            page=page, per_page=per_page, ids=careers.collect(lambda each: each.id), only_ids=False)

    elif user.is_cathedra_manager():

        kwargs["messages"] = {
            "assigned": "Cátedras Asignadas",
            "to_assign": "Cátedras Disponibles"
        }

        form = CathedraSeeker(request.args)

        kwargs["workplace"] = "cathedra"
        kwargs["assigned_elements"] = user.get_cathedras()
        args = {
            "career_list_id": form.career_list.data,
            "name": form.name.data if form.name.data != "" else None,
            "page": page,
            "per_page": per_page,
            "ids": user.get_cathedras().collect(lambda each: each.id),
            "only_ids": False
        }
        kwargs["elements_to_assign"] = Cathedra.search_form(**args)

    else:

        kwargs["messages"] = {
            "assigned": "Oficinas Asignadas",
            "to_assign": "Oficinas Disponibles"
        }

        form = OfficeSeeker(request.args)

        kwargs["workplace"] = "office"
        kwargs["assigned_elements"] = user.get_offices()
        args = {
            "name": form.name.data if form.name.data != "" else None,
            "page": page,
            "per_page": per_page,
            "ids": user.get_offices().collect(lambda each: each.id),
            "only_ids": False
        }
        kwargs["elements_to_assign"] = Office.search_form(**args)

    return render_template("user/assignment.html", form=form, **kwargs)


@permission('user_content_assign')
def assign(user_id, element_id):

    user = User.get(user_id)

    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    if not user.is_responsible():
        add_alert(Alert("danger", "El usuario no es responsable de elementos."))
        return redirect(url_for("user_index"))

    if user.is_career_manager():
        element = Career.get(element_id)
    elif user.is_cathedra_manager():
        element = Cathedra.get(element_id)
    else:
        element = Office.get(element_id)

    if not element:
        add_alert(Alert("danger",
                        f"La {user.get_responsible_content_label()} especificada no existe."))
        return redirect(url_for("user_content_index", user_id=user_id))

    user.add_responsible_element(element)
    user.save()
    add_alert(
        Alert("success", f'La {user.get_responsible_content_label()} "{element.name}" fue asignada con éxito.'))

    return redirect(url_for("user_content_index", user_id=user_id))


@permission('user_content_unassign')
def unassign(user_id, element_id):

    user = User.get(user_id)

    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    if not user.is_responsible():
        add_alert(Alert("danger", "El usuario no es responsable de elementos."))
        return redirect(url_for("user_index"))

    if user.is_career_manager():
        element = Career.get(element_id)
    elif user.is_cathedra_manager():
        element = Cathedra.get(element_id)
    else:
        element = Office.get(element_id)

    if not element:
        add_alert(Alert("danger",
                        f"La {user.get_responsible_content_label()} especificada no existe."))
        return redirect(url_for("user_content_index", user_id=user_id))

    user.remove_responsible_element(element)
    user.save()
    add_alert(
        Alert("success", f'La {user.get_responsible_content_label()} "{element.name}" fue desasignada con éxito.'))

    return redirect(url_for("user_content_index", user_id=user_id))
