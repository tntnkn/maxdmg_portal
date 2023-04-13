from flask      import current_app as app
from flask      import render_template, redirect, url_for, flash

from .auth      import UserAuth, current_user, login_required 
from .forms     import (RegisterUserForm, LoginUserForm, 
                        RequestResetPasswordForm, ResetPasswordForm, 
                        AddGraphCredentialsForm)
from .storage   import storage, Models


@app.route('/')
@login_required
def home():
    return render_template(
                'home.html',
                title='Домашняя страница',
            )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    form = LoginUserForm()
    if form.validate_on_submit():
        usr = storage.GetUser('email', form.email.data)
        if usr and \
           UserAuth.CheckPassword(form.password.data, usr.password):
            UserAuth(usr.id).Login()
            flash('Добро пожаловать!',
                  'success')
            return redirect( url_for('home') )
        flash('Что-то не так с вашими данными. Попробуйте ещё раз.', 
              'warning')
        return redirect( url_for('login') )
    return render_template(
                'login.html',
                title='Вход',
                form=form,
                hide_header=True,
            )

@app.route('/logout')
@login_required
def logout():
    UserAuth.Logout()
    return redirect( url_for('login') )

@app.route('/request_reset_password', methods=['GET', 'POST'])
def request_reset_password():
    form = RequestResetPasswordForm() 
    if form.validate_on_submit():
        usr = storage.GetUser('email', form.email.data)
        if usr:
            pass
        flash('Если Вы зарегистрированы, то на указанный имейл придёт письмо с инструкциями по смене пароля.',
              'info')
        return redirect( url_for('home') )
    return render_template(
                'request_reset_password.html',
                title='Страница смены пароля',
                form=form
           )

@app.route('/reset_password_user_logged_in', methods=['GET', 'POST'])
@login_required
def reset_password_user_logged_in():
    u_id = UserAuth.GetCurUserId()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        usr  = storage.GetUser('id', u_id)
        if UserAuth.CheckPassword(form.password.data, usr.password):
            flash(f"Этот пароль уже используется. Попробуйте другой.", 
                  'warning')
            return redirect( url_for('reset_password_user_logged_in') )
        new_password=UserAuth.HashPassword(form.password.data)
        storage.UpdateUserPassword(u_id, new_password)
        UserAuth.Logout()
        flash("Ваш пароль обновлён!", 
              'success')
        return redirect( url_for('login') )
    return render_template(
                'reset_password.html',
                title='Страница смены пароля',
                form=form
           )


@app.route('/account')
@login_required
def account():
    u_id = UserAuth.GetCurUserId()
    usr  = storage.GetUser('id', u_id)
    return render_template(
                'account.html',
                title='Профиль',
                user_info=usr,
           )

@app.route('/instruments')
@login_required
def instruments():
    u_id = UserAuth.GetCurUserId()
    usr  = storage.GetUser('id', u_id)
    return render_template(
                'instruments.html',
                title='Инструменты',
                user_info=usr,
           )

@app.route('/admin')
@login_required
def admin():
    if not UserAuth.UserIsAdmin():
        return redirect( url_for('home') )
    return render_template('admin.html',
                           title='Панель админа')

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def admin_add_user():
    u_id = UserAuth.GetCurUserId()
    usr  = storage.GetUser('id', u_id)
    if not usr.is_admin:
        return redirect( url_for('home') )
    form = RegisterUserForm()
    if form.validate_on_submit():
        usr = Models.User(
            id=-1,
            name=form.name.data,
            password=UserAuth.HashPassword(form.password.data),
            email=form.email.data,
            is_admin=False
        )
        if storage.CreateUser(usr):
            flash(f"Пользователь {usr.name} добавлен!", 
                  'success')
        else:
            flash(f"Не получилось добавить пользователя {usr.name}!",
                  'warning')
        return redirect( url_for('admin_add_user') )
    return render_template('admin_add_user.html',
                           form=form,
                           title='Создание пользователя')

@app.route('/admin/add_graph', methods=['GET', 'POST'])
@login_required
def admin_add_graph():
    u_id = UserAuth.GetCurUserId()
    usr  = storage.GetUser('id', u_id)
    if not usr.is_admin:
        return redirect( url_for('home') )
    form = AddGraphCredentialsForm()
    if form.validate_on_submit():
        g_crd = Models.GraphCredentials(
            id      =-1,
            user_id =-1,
            name    =form.name.data,
            airtable_api_key=\
                    form.airtable_api_key.data,
            airtable_base_id=\
                    form.airtable_base_id.data,
            airtable_states_table_id=\
                    form.airtable_states_table_id.data,
            airtable_states_table_view_id=\
                    form.airtable_states_table_view_id.data,
            airtable_transitions_table_id=\
                    form.airtable_transitions_table_id.data,
            airtable_transition_table_view_id=\
                    form.airtable_transition_table_view_id.data,
            airtable_forms_table_id=\
                    form.airtable_forms_table_id.data,
            airtable_forms_table_view_id=\
                    form.airtable_forms_table_view_id.data,
            airtable_config_table_id=\
                    form.airtable_config_table_id.data,
            airtable_config_table_view_id=\
                    form.airtable_config_table_view_id.data
        )
        if storage.CreateGraph(g_crd):
            flash(f"Граф {g_crd.name} добавлен!", 'success')
        else:
            flash(f"Не получилось добавить граф {g_crd.name}!", 
                  'warning')
        return redirect( url_for('admin_add_graph') )
    return render_template('admin_add_graph.html',
                           form=form,
                           title='Добавление графа')
