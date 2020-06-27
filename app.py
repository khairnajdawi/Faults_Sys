import os
from flask import Flask,render_template, request, Response, flash, redirect, url_for,jsonify,abort
from flask_cors import CORS
from models import db,setup_db,Branches
from flask_moment import Moment
from flask_wtf import FlaskForm
from forms import *


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return render_template('pages/home.html')

    
    @app.route('/branches')
    def branches():
        branches = Branches.query.all()
        return render_template('pages/branches/branches.html',branches=branches)

    @app.route('/branches/add')
    def add_branch():
        form = AddBrancheForm()
        return render_template('pages/branches/add.html',form=form)

    @app.route('/branches/add',methods=['POST'])
    def add_new_branch():
        form = AddBrancheForm(request.form)
        new_branch = Branches(name=form.name.data)
        #suppose succes is false
        success=False
        try:
            db.session.add(new_branch)
            db.session.commit()
            #if commit succes is true
            success=True
            # on successful db insert, flash success
            flash('Branch \"' + new_branch.name + '\" was successfully added!','success')
        except:
            #if failed for any reason then rollback
            db.session.rollback()
            flash('An error occurred. Branch \"' + new_branch.name + '\" could not be added.','danger')
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        finally:
            db.session.close()

        #if success return to homepage else stay at new venue form
        if(success):
            return redirect(url_for('branches'))
        else:
            return render_template('pages/branches/add.html', form=form)
    

    @app.route('/branches/<int:branch_id>/edit')
    def edit_branch(branch_id):
        form = EditBrancheForm()
        branch = Branches.query.get(branch_id)
        form.is_active.data = "True" if branch.is_active else "False"
        return render_template('pages/branches/edit.html',form=form,branch=branch)


    @app.route('/branches/<int:branch_id>/edit',methods=['POST'])
    def update_branch(branch_id):
        form = EditBrancheForm(request.form)
        branch = Branches.query.get(branch_id)
        #suppose succes is false
        success=False
        try:
            branch.name = form.name.data
            branch.is_active = form.is_active.data=="True"
            db.session.add(branch)
            db.session.commit()
            #if commit succes is true
            success=True
            # on successful db insert, flash success
            flash('Branch \"' + branch.name + '\" was successfully updated!','success')
        except:
            #if failed for any reason then rollback
            db.session.rollback()
            flash('An error occurred. Branch \"' + branch.name + '\" could not be edited.','danger')
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        finally:
            db.session.close()

        #if success return to homepage else stay at new venue form
        if(success):
            return redirect(url_for('branches'))
        else:
            return render_template('pages/branches/edit.html', form=form,branch=branch)


    @app.route('/branches/<int:branch_id>')
    def branch_info(branch_id):
        branch = Branches.query.get(branch_id)
        return render_template('pages/branches/info.html',branch=branch)


    @app.route('/branches/<int:branch_id>/delete')
    def confirm_delete_branch(branch_id):
        branch = Branches.query.get(branch_id)
        # TODO : check if branch has a faults        
        return render_template('pages/branches/delete.html',branch=branch)

    @app.route('/branches/<int:branch_id>/delete',methods=['POST'])
    def delete_branch(branch_id):
        #suppose succes is false
        success=False
        branch = Branches.query.get(branch_id)
        try:
            db.session.delete(branch)
            db.session.commit()
            success=True
        except:
            db.rollback()
            success=False
        finally:
            db.session.close()

        #if success return to homepage else stay at new venue form
        if(success):
            flash('Branch \"' + branch.name + '\" deleted successfully!','success')
            return redirect(url_for('branches'))
        else:            
            flash('Branch \"' + branch.name + '\" could not be deleted!','danger')
            return render_template('pages/branches/delete.html',branch=branch)
        # TODO : check if branch has a faults        
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
