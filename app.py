import os
from flask import Flask,render_template, request, Response, flash, redirect, url_for,jsonify,abort
from flask_cors import CORS
from models import db,setup_db,Branches,FaultTypes,ITSections
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
        form = AddBranchForm()
        return render_template('pages/branches/add.html',form=form)

    @app.route('/branches/add',methods=['POST'])
    def add_new_branch():
        form = AddBranchForm(request.form)
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
        finally:
            db.session.close()

        if(success):
            return redirect(url_for('branches'))
        else:
            return render_template('pages/branches/add.html', form=form)
    

    @app.route('/branches/<int:branch_id>/edit')
    def edit_branch(branch_id):
        form = EditBranchForm()
        branch = Branches.query.get(branch_id)
        form.is_active.data = "True" if branch.is_active else "False"
        return render_template('pages/branches/edit.html',form=form,branch=branch)


    @app.route('/branches/<int:branch_id>/edit',methods=['POST'])
    def update_branch(branch_id):
        form = EditBranchForm(request.form)
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
        finally:
            db.session.close()

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

        if(success):
            flash('Branch \"' + branch.name + '\" deleted successfully!','success')
            return redirect(url_for('branches'))
        else:            
            flash('Branch \"' + branch.name + '\" could not be deleted!','danger')
            return render_template('pages/branches/delete.html',branch=branch)
        # TODO : check if branch has a faults   


    @app.route('/itsections')
    def itsections():
        itsections = ITSections.query.all()    
        return render_template('pages/itsections/sectionslist.html',itsections=itsections)


    @app.route('/itsections/add')
    def add_it_section_form():
        form = AddITSectionForm()
        return render_template('pages/itsections/add.html',form=form)



    @app.route('/itsections/add',methods=['POST'])
    def add_it_section():
        form = AddITSectionForm(request.form)
        success=False
        new_section = ITSections(name=form.name.data)
        try:
            db.session.add(new_section)
            db.session.commit()
            success=True
            flash('IT Section \"' + new_section.name + '\" added successfully!','success')
        except:
            db.session.rollback()
            flash('IT Section \"' + new_section.name + '\" could not be added','danger')
        finally:
            db.session.close()
        if(success):
            return redirect(url_for('itsections'))
        else:            
            return render_template('pages/itsections/add.html',form=form)

    @app.route('/itsections/<int:section_id>')
    def section_info(section_id):
        section = ITSections.query.get(section_id)
        return render_template('pages/itsections/info.html',section=section)


    @app.route('/itsections/<int:section_id>/edit')
    def edit_section_form(section_id):
        form = EditITSectionForm()
        section = ITSections.query.get(section_id)
        form.name.data=section.name
        form.is_active.data = "True" if section.is_active else "False"
        return render_template('pages/itsections/edit.html',form=form,section=section)


    @app.route('/itsections/<int:section_id>/edit',methods=['POST'])
    def edit_section(section_id):
        form = EditITSectionForm(request.form)
        section = ITSections.query.get(section_id)
        success=False
        try:
            section.name = form.name.data
            section.is_active = form.is_active.data=="True"
            db.session.commit()
            success=True
            flash('IT Section \"' + section.name + '\" updated successfully!','success')
        except:
            db.session.rollback()
            flash('IT Section \"' + section.name + '\" could not be updated','danger')
        finally:
            db.session.close()

        if(success):
            return redirect(url_for('itsections'))
        else:
            return render_template('pages/itsections/edit.html',form=form,section=section)

    @app.route('/itsections/<int:section_id>/delete')
    def delete_section_form(section_id):
        section = ITSections.query.get(section_id)
        return render_template('pages/itsections/delete.html',section=section)


    @app.route('/itsections/<int:section_id>/delete',methods=['POST'])
    def delete_section(section_id):
        section = ITSections.query.get(section_id)
        deleted = False
        try:
            db.session.delete(section)
            db.session.commit()
            deleted = True
            flash('IT Section \"' + section.name + '\" deleted successfully!','success')
        except:
            db.session.rollback()
            flash('IT Section \"' + section.name + '\" could not be deleted!','danger')
        finally:
            db.session.close()

        if(deleted):
            return redirect(url_for('itsections'))
        else:
            return render_template('pages/itsections/edit.html',section=section)


    @app.route('/faulttypes')
    def faulttypes():
        types = db.session.query(FaultTypes.id,FaultTypes.fault_type,FaultTypes.is_active,ITSections.name.label("section_name"))\
            .outerjoin(ITSections,FaultTypes.it_section==ITSections.id)\
            .all()    
        return render_template('pages/faults/typeslist.html',types=types)

    @app.route('/faulttypes/<int:type_id>')
    def faulttypes_info(type_id):
        fault_type = db.session.query(FaultTypes.id,FaultTypes.fault_type,FaultTypes.is_active,ITSections.name.label("section_name"))\
            .outerjoin(ITSections,FaultTypes.it_section==ITSections.id)\
            .filter(FaultTypes.id==type_id)\
            .one_or_none() 
        return render_template('pages/faults/info.html',fault_type=fault_type)



    @app.route('/faulttypes/add')
    def add_faulttypes_form(): 
        form = AddFaultTypeForm()
        return render_template('pages/faults/add.html',form=form)


    @app.route('/faulttypes/add',methods=['POST'])
    def add_faulttypes(): 
        form = AddFaultTypeForm(request.form)
        new_type = FaultTypes(
            fault_type=form.fault_type.data,
            it_section=form.it_section.data
            )
        success=False
        try:
            db.session.add(new_type)
            db.session.commit()            
            success=True
            flash('Fault Type : \"' + new_type.fault_type + '\" added successfully!','success')
        except:
            db.session.rollback()
            flash('Fault Type : \"' + new_type.fault_type + '\" could not be added!','danger')
        finally:
            db.session.close()

        if(success):
            return redirect(url_for('faulttypes'))
        else:
            return render_template('pages/faults/add.html',form=form)


    @app.route('/faulttypes/<int:type_id>/edit')
    def edit_faulttypes_form(type_id): 
        form = EditFaultTypeForm()
        fault_type = FaultTypes.query.get(type_id)
        form.fault_type.data =fault_type.fault_type
        form.it_section.data = fault_type.it_section
        return render_template('pages/faults/edit.html',form=form)


    @app.route('/faulttypes/<int:type_id>/edit',methods=['POST'])
    def edit_faulttypes(type_id): 
        form = EditFaultTypeForm(request.form)
        fault_type = FaultTypes.query.get(type_id)
        updated=False
        try:
            fault_type.fault_type = form.fault_type.data
            fault_type.it_section = form.it_section.data
            db.session.commit()
            updated=True
            flash('Fault Type : \"' + fault_type.fault_type + '\" updated successfully!','success')
        except:
            db.session.rollback()
            flash('Fault Type : \"' + fault_type.fault_type + '\" could not be updated!','danger')
        finally:
            db.session.close()

        if(updated):
            return redirect(url_for('faulttypes'))
        else:
            return render_template('pages/faults/edit.html',form=form)


    @app.route('/faulttypes/<int:type_id>/delete')
    def delete_faulttypes_form(type_id): 
        fault_type = FaultTypes.query.get(type_id)
        return render_template('pages/faults/delete.html',fault_type=fault_type)


    @app.route('/faulttypes/<int:type_id>/delete',methods=['POST'])
    def delete_faulttypes(type_id): 
        fault_type = FaultTypes.query.get(type_id)
        deleted = False
        try:
            db.session.delete(fault_type)
            db.session.commit()
            deleted=True
            flash('Fault Type : \"' + fault_type.fault_type + '\" deleted successfully!','success')
        except:
            db.session.rollback()
            flash('Fault Type : \"' + fault_type.fault_type + '\" could not be deleted!','danger')
        finally:
            db.session.close()

        if(deleted):
            return redirect(url_for('faulttypes'))
        else:
            return render_template('pages/faults/delete.html',fault_type=fault_type)



    return app

app = create_app()

if __name__ == '__main__':
    app.run()
