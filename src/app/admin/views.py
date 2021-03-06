from app.admin import admin
from app.admin.forms import CatalogItemForm
from app.decorators import demo_admin_required
from app.extensions import db
from app.models import (
    CatalogItem,
    Category,
)
from flask import (
    flash,
    redirect,
    render_template,
    url_for
)
from flask_login import login_required


@admin.before_request
@login_required
@demo_admin_required
def require_login():
    pass


@admin.route('/')
@admin.route('/index')
def index():
    catalog_items = CatalogItem.query.all()
    return render_template('admin/index.html',
                           catalog_items=catalog_items,
                           title='Catalog Items')


@admin.route('/new', methods=['GET', 'POST'])
def new():
    categories = Category.query \
        .all()
    form = CatalogItemForm()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    if form.validate_on_submit():
        catalog_item = CatalogItem()
        form.populate_obj(catalog_item)
        db.session.add(catalog_item)
        db.session.commit()
        flash('Catalog Item is added!', 'success')
        return redirect(url_for('admin.index'))

    return render_template('admin/new.html',
                           form=form,
                           title='Catalog Items')


@admin.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    catalog_item = CatalogItem.query \
        .filter_by(id=id) \
        .first_or_404()
    categories = Category.query \
        .all()
    form = CatalogItemForm(obj=catalog_item)
    form.category_id.choices = [
        (m.id, m.name) for m in categories]
    if form.validate_on_submit():
        form.populate_obj(catalog_item)
        db.session.add(catalog_item)
        db.session.commit()
        flash('Catalog Item is updated!', 'success')
        return redirect(url_for('admin.index'))

    cateogires = Category.query.all()

    return render_template('admin/edit.html',
                           categories=categories,
                           catalog_item=catalog_item,
                           form=form,
                           title='Catalog Items')


@admin.route('/details/<id>')
def details(id):
    catalog_item = CatalogItem.query \
        .filter_by(id=id) \
        .first_or_404()

    return render_template('admin/details.html',
                           catalog_item=catalog_item,
                           title='Catalog Items')
