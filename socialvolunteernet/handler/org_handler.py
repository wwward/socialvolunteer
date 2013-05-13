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
        org_id = int(self.request.get('organization_id'))
        logging.info("Received POST request, action="+repr(actions)+" chose="+action+" kind="+self.request.get('kind'))
        if not action:
            self.response.out.write(str(template.render("web/signup_organization.html", {})))
            
        if action.lower() == "complete_volunteers":
            logging.info("Complete: "+repr(self.request.get_all('completed')))
            self.volunteer_complete(self.request.get_all('completed'))
            
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
        elif action.lower() == 'modify_job' and self.request.get('kind') == 'delete':   
            # Some weird nested forms issue I don't feel like looking at.
            # TODO: Perhaps we need to use named forms.
            # TODO: Something funky is going on here. Too many ids are being deleted
            logging.info("DELETE JOB: "+repr(self.request.get_all('job_id')))
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
        elif action.lower() == 'modify_job' and self.request.get('kind') == 'edit':
            # TODO: More weirdness.... this is actually doing a delete.
            job_ids = [int(i) for i in self.request.get_all('selected_jobs')]

            if not job_ids:
                logging.info("EDIT JOB: (no job ids)")
                portal = self.get_organization_portal(org_id)
                self.response.out.write(str(template.render("web/organization.html", portal)))
            else:   
                logging.info("EDIT JOB: "+repr(job_ids))

                job_data = {'jobs' : self.get_job_display(job_ids)}
                job_data['organization_id'] = org_id
                job_data['job_ids'] = job_ids
                logging.info("Job data: "+repr(job_data))

                self.response.out.write(str(template.render("web/edit_job.html", job_data)))

        elif action.lower() == "edit_submit_job":
            #TODO: Add error checking to the edit portal
            #TODO: Only one job gets submitted at a time
            job_ids = [int(i) for i in self.request.get('job_ids').split(',')]
            job_id = int(self.request.get('job_id'))
            org_id = int(self.request.get('organization_id'))

            params = {}
            params['job_id'] = job_id
            params['organization_id'] = org_id
            params['title'] = self.request.get('title')
            params['description'] = self.request.get('description')
            params['time'] = self.request.get('time')
            params['location'] = self.request.get('location')
            params['date'] = self.request.get('date')
            params['duration'] = self.request.get('duration')
            params['difficulty'] = self.request.get('difficulty')
            params['category'] = self.request.get('category')
            params['status'] = self.request.get('status')
            params['keywords'] = [ t.strip() for t in self.request.get('keywords').split(',')]
            

            logging.info("Params from page: "+repr(params))
            missing = self.edit_job(**params)
            #if missing:
            #    logging.info("MISSING: "+repr(missing))
            #    self.response.out.write(str(template.render("web/edit_job.html", {"organization_id": org_id, "missing": missing})))
            #else:
            job_data = {'jobs' : self.get_job_display(job_ids)}
            job_data['organization_id'] = org_id
            job_data['job_ids'] = job_ids
            logging.info("New display data: "+repr(job_data))
            self.response.out.write(str(template.render("web/edit_job.html", job_data)))
        elif action.lower() == "edit_organization":
            data = self.get_info(org_id)
            data['organization_id'] = org_id
            self.response.out.write(str(template.render("web/edit_organization.html", data)))
        elif action.lower() == "submit_edit_organization":
            name = self.request.get('name')
            description = self.request.get('description')
            phone = self.request.get('phone')
            email = self.request.get('email')
            location = self.request.get('location')
            self.edit_organization(org_id, name, description, phone, location, email)
            data = self.get_info(org_id)
            data['organization_id'] = org_id
            self.response.out.write(str(template.render("web/edit_organization.html", data)))

        elif action.lower() == "portal":
            portal = self.get_organization_portal(org_id)
            self.response.out.write(str(template.render("web/organization.html", portal)))
    
    # Implemented by parent class, but we don't want to allow gets            
    def get(self):
        logging.error("GET METHOD NOT SUPPORTED")
        raise Exception("GET METHOD NOT SUPPORTED")
            
    def edit_organization(self, org_id, name, description, phone, location, email):
        missing = []
        if not name:
            missing.append("name")
        if not description:
            missing.append("description")
        if not phone:
            missing.append("phone")
        if not location:
            missing.append("location")
        if not email:
            missing.append("email")
        if not missing:
            self.org.edit_organization_data(organization_id=org_id, name=name, location=location, description=description, email=email, phone=phone)
            logging.info("EDIT ORGANIZATION "+name+" "+description+" "+str(org_id)+" "+location+" "+email)
        return missing  
    
    def get_organization_portal(self, organization_id):
        response = self.org.get_info(organization_id)[0]
        response['organization_id'] = organization_id
        response["current_commitments"] = self.org.get_unreviewed_jobs(organization_id)
        response["current_jobs"] = self.org.get_current_jobs(organization_id)
        response["upcoming_commitments"] = self.org.get_committed_jobs(organization_id)
        response["completed_jobs"] = self.org.get_completed_jobs(organization_id)   
        response['organization_id'] = organization_id
        return response
        
    def get_info(self, organization_id):
        return self.org.get_info(organization_id)[0]
        
    def get_job_display(self, job_ids):
        jobs = []
        for job_id in job_ids:
            job_data = self.job.get_info(job_id)[0]
            jobs.append(job_data)
            logging.info("Job display data: "+repr(job_data))
        return jobs
    
    def volunteer_complete(self, completed_list):
        for completed in completed_list:
            completed = completed.split(',')                
            if len(completed) == 2:

                self.job.volunteer_completed(int(completed[0]), int(completed[1]))
                logging.info("COMPLETED volunteer_id:"+completed[0]+" job_id:"+completed[1])
        
    def cancel_volunteer(self, volunteers):
        for volunteer in volunteers:
            pieces = volunteer.split(",")
            if len(pieces) == 2:
                self.job.delete_volunteer(int(pieces[0]), int(pieces[1]))
                logging.info("DELETED VOLUNTEER volunteer_id:"+pieces[0]+" job_id:"+pieces[1])
        
    def delete_job(self, job_ids, organization_id):
        logging.info('job'+repr(job_ids))

        for job_id in job_ids:
            logging.info('job'+repr(job_id))
            if len(job_id) > 0:
                self.org.delete_job(organization_id, int(job_id))
                logging.info("DELELTED JOB organization_id:"+repr(organization_id)+" job_id:"+repr(job_id))

    def add_job(self, **kw):
        missing = self.check_job_values(kw)
        #if not missing:
        kw['score'] = self.calculate_score(kw['duration'], kw['difficulty'])
        self.job.create_new(**kw)
        logging.info("CREATE JOB "+kw['title'])
        return missing        
    
    def edit_job(self, **kw):
        missing = self.check_job_values(kw)
        #if not missing:
        kw['score'] = self.calculate_score(kw['duration'], kw['difficulty'])
        self.job.edit_job(**kw)
        logging.info("EDIT JOB "+repr(kw))
        return missing 
    
    def calculate_score(self, duration, difficulty):
        return int(duration) * int(difficulty)
    
    def check_job_values(self, params) :
        missing = []
        for param in ("description", "time", "location", "date", "title", "duration", "difficulty", "category", "keywords"):
            if not param in params:   
                missing.append(param)
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