from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Application
from app.main.forms import ApplicationForm
from app.main.forms import ApplicationForm, UpdateProfileForm, ChangePasswordForm
from app import db, bcrypt


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    stats = {
        'total_users': User.query.count(),
        'total_applications': Application.query.count()
    }
    return render_template('home.html', title='Home', stats=stats)


@main.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status_filter = request.args.get('status', 'All')
    per_page = 5

    query = Application.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(
            Application.company.ilike(f'%{search}%') |
            Application.role.ilike(f'%{search}%')
        )

    if status_filter != 'All':
        query = query.filter_by(status=status_filter)

    pagination = query.order_by(
        Application.date_applied.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    applications = pagination.items

    all_applications = Application.query.filter_by(user_id=current_user.id).all()

    stats = {
        'total': len(all_applications),
        'applied': len([a for a in all_applications if a.status == 'Applied']),
        'interviews': len([a for a in all_applications if a.status == 'Interview']),
        'offers': len([a for a in all_applications if a.status == 'Offer']),
        'rejected': len([a for a in all_applications if a.status == 'Rejected'])
    }

    return render_template('main/dashboard.html',
        title='Dashboard',
        applications=applications,
        stats=stats,
        status_filter=status_filter,
        pagination=pagination,
        search=search
    )


@main.route('/application/new', methods=['GET', 'POST'])
@login_required
def new_application():
    form = ApplicationForm()
    
    if form.validate_on_submit():
        application = Application(
            company=form.company.data,
            role=form.role.data,
            status=form.status.data,
            location=form.location.data,
            job_type=form.job_type.data,
            salary=form.salary.data,
            source=form.source.data,
            notes=form.notes.data,
            user_id=current_user.id
        )

        db.session.add(application)
        db.session.commit()
        flash('Application added!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/new_application.html', title='Add Application', form=form)

@main.route('/application/edit/<int:application_id>', methods=['GET', 'POST'])
@login_required
def edit_application(application_id):
    application = Application.query.get_or_404(application_id)

    if application.user_id != current_user.id:
        flash('You cannot edit the application','danger')
        return redirect(url_for('main.dashboard'))
    
    form  = ApplicationForm()

    if form.validate_on_submit():
        application.company = form.company.data
        application.role = form.role.data
        application.status = form.status.data
        application.notes = form.notes.data
        db.session.commit()
        flash('Application updated!', 'success')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'GET':
        form.company.data = application.company
        form.role.data = application.role
        form.status.data = application.status
        form.notes.data = application.notes

    return render_template('main/edit_application.html', title='Edit Application', form=form, application=application)


@main.route('/application/delete/<int:application_id>', methods=['POST'])
@login_required
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    
    # Security check — make sure user owns this application
    if application.user_id != current_user.id:
        flash('You cannot delete this application.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted.', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = UpdateProfileForm()
    password_form = ChangePasswordForm()

    if profile_form.validate_on_submit() and request.form.get('form_type') == 'update_profile':
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.college = profile_form.college.data
        current_user.branch = profile_form.branch.data
        current_user.graduation_year = profile_form.graduation_year.data
        current_user.cgpa = profile_form.cgpa.data
        current_user.backlogs = profile_form.backlogs.data
        current_user.internship_count = profile_form.internship_count.data
        current_user.project_count = profile_form.project_count.data
        current_user.skills = profile_form.skills.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('main.profile'))

    if password_form.validate_on_submit() and request.form.get('form_type') == 'change_password':
        if bcrypt.check_password_hash(current_user.password, password_form.current_password.data):
            current_user.password = bcrypt.generate_password_hash(
                password_form.new_password.data
            ).decode('utf-8')
            db.session.commit()
            flash('Password changed!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Current password is incorrect.', 'danger')

    if request.method == 'GET':
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.college.data = current_user.college
        profile_form.branch.data = current_user.branch
        profile_form.graduation_year.data = current_user.graduation_year
        profile_form.cgpa.data = current_user.cgpa
        profile_form.backlogs.data = current_user.backlogs
        profile_form.internship_count.data = current_user.internship_count
        profile_form.project_count.data = current_user.project_count
        profile_form.skills.data = current_user.skills

    total_apps = Application.query.filter_by(user_id=current_user.id).count()

    return render_template('main/profile.html',
        title='Profile',
        profile_form=profile_form,
        password_form=password_form,
        total_apps=total_apps
    )