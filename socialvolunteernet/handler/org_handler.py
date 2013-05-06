import logging

from socialvolunteernet.model.organization import Organization
from socialvolunteernet.model.job import Job

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import wsgiref.handlers


class OrganizationHandler(webapp.RequestHandler):

    org = Organization()
    job = Job({})        
        
    def post(self):
        actions = self.request.get_all('action')
        action = actions[-1]
        org_id = self.request.get('organization_id')
        logging.info("Received POST request, action="+repr(actions)+" chose="+action)
        if not action:
            self.response.out.write(str(template.render("web/signup_organization.html", {})))
            
        if action.lower() == "complete_volunteers":
            self.volunteer_complete(self.request.get_all('completed'))
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "edit_job" and self.request.get('kind') == 'delete':   
            # Some weird nested forms issue I don't feel like looking at.
            # TODO: Perhaps we need to use named forms.
            # TODO: Something funky is going on here. Too many ids are being deleted
            self.delete_job(self.request.get_all('job_id'), org_id)
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "cancel_volunteer":
            #TODO: The checkbox issue
            self.cancel_volunteer(self.request.get_all('volunteers'))
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "new_job":
            self.response.out.write(str(template.render("web/create_job.html", {"organization_id": org_id})))
        elif action.lower() == "create_submit_job":
            name = self.request.get('name')
            description = self.request.get('description')
            date = self.request.get('date')
            time = self.request.get('time')
            location = self.request.get('location')
            missing = self.add_job(name, description, time, location, date)
            if missing:
                logging.info("missing "+repr(missing))
                self.response.out.write(str(template.render("web/create_job.html", {"organization_id": org_id, "missing": missing})))
            else:
                portal = self.get_organization_portal(org_id)
                self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "edit_job":
            # TODO: More weirdness.... this is actually doing a delete.
            job_id = self.request.get('job_id')
            job_data = self.get_job_display(job_id)
            self.response.out.write(str(template.render("web/edit_job.html", job_data)))
        elif action.lower() == "edit_submit_job":
            #TODO: Add error checking to the edit portal
            job_id = self.request.get('job_id')
            name = self.request.get('name')
            description = self.request.get('description')
            time = self.request.get('time')
            location = self.request.get('location')
            missing = self.edit_job(job_id, sname, description, time, location)
            if missing:
                self.response.out.write(str(template.render("web/edit_job.html", {"organization_id": org_id, "missing": missing})))
            else:
                portal = self.get_organization_portal(org_id)
                self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == "edit_organization":
            data = self.get_info(org_id)
            self.response.out.write(str(template.render("web/edit_organization.html", data)))
        elif action.lower() == "submit_edit_organization":
            name = self.request.get('name')
            description = self.request.get('description')
            phone = self.request.get('phone')
            location = self.request.get('location')
            self.edit_organization(org_id, name, description, phone, location)
            data = self.get_info(org_id)
            self.response.out.write(str(template.render("web/edit_organization.html", data)))

        elif action.lower() == "portal":
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
    
    # Implemented by parent class, but we don't want to allow gets            
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
            
    def edit_organization(self, org_id, name, description, phone, location):
        missing = []
        if not name:
            missing.append("name")
        if not description:
            missing.append("description")
        if not phone:
            missing.append("phone")
        if not location:
            missing.append("location")
        if not missing:
            self.org.edit_organization_data(org_id, name=name, location=location, description=description)
            logging.info("EDIT ORGANIZATION "+name+" "+description+" "+org_id+" "+location)
        return missing 
    
    def get_organization_portal(self, organization_id):
        response = self.org.get_info(organization_id)[0]
        response["current_commitments"] = self.org.get_unreviewed_jobs(organization_id)
        response["current_jobs"] = self.org.get_current_jobs(organization_id)
        response["upcoming_commitments"] = self.org.get_committed_jobs(organization_id)
        response["completed_jobs"] = self.org.get_completed_jobs(organization_id)   
        logging.info(repr(response)) 
        return response
        
    def get_info(self, organization_id):
        return self.org.get_info(organization_id)[0]
        
    def get_job_display(self, job_id):
        return self.job.get_info(job_id)
    
    def volunteer_complete(self, completed_list):
        for completed in completed_list:
            completed = completed.split(',')                
            if len(completed) == 2:
                self.job.volunteer_completed(completed[0], completed[1])
                logging.info("COMPLETED volunteer_id:"+completed[0]+" job_id:"+completed[1])
        
    def cancel_volunteer(self, volunteers):
        for volunteer in volunteers:
            pieces = volunteer.split(",")
            if len(pieces) == 2:
                self.job.delete_volunteer(pieces[0], pieces[1])
                logging.info("DELETED VOLUNTEER volunteer_id:"+volunteer_id+" job_id:"+job_id)
        
    def delete_job(self, job_ids, organization_id):
        for job_id in job_ids:
            self.org.delete_job(organization_id, job_id)
            logging.info("DELELTED JOB organization_id:"+organization_id+" job_id:"+job_id)

    def add_job(self, name, description, time, location, date):
        missing = []
        if not name:
            missing.append("name")
        if not description:
            missing.append("description")
        if not time:
            missing.append("time")
        if not location:
            missing.append("location")
        if not date:
            missing.append("date")
        if not missing:
            self.job.create_new(name=name, time=time, location=location, description=description, date=date)
            logging.info("CREATE JOB "+name+" "+description+" "+time+" "+location+" "+date)
        return missing        
    
    def edit_job(self, job_id, name, description, time, location):
        missing = []
        if not name:
            missing.append("name")
        if not description:
            missing.append("description")
        if not time:
            missing.append("time")
        if not location:
            missing.append("location")
        if not date:
            missing.append("date")
        if not missing:
            self.job.edit_job(job_id=job_id, name=name, time=time, location=location, description=description, date=date)
            logging.info("EDIT JOB "+name+" "+description+" "+time+" "+location+" "+date)
        return missing 
    
        
    def parse_param(self, name, value, params):
        params[name] = value
        if not name:
            params['error'] = True
            params['missing'].append(name)


def main():
    app = webapp.WSGIApplication([('/org', OrganizationHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app) 
    
if __name__ == "__main__":
    main()