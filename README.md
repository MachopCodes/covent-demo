# CoVent - Sponsor and Event Organizer Platform

CoVent connects **sponsors looking for events** and **event organizers looking for sponsors**. This platform allows sponsors to showcase their sponsorship profiles while enabling event organizers to submit tailored event proposals. 

---

# Front End Deployment
https://covent-frontend.vercel.app/

# Backend Deployment
https://covent-demo.vercel.app/

## for swagger docs
https://covent-demo.vercel.app/docs

## Features

### **1. Sponsor Profile Page**
- Displays sponsor information such as:
  - Budget range
  - Target audience (e.g., buyer personas, industries)
  - Key objectives for event sponsorship
- Each sponsor profile is accessible via a unique, shareable URL.

### **2. Event Proposal Submission**
- **Grid/List View of Sponsors:** Browse all sponsors in a simple layout.
- **Proposal Submission Form:**
  - Input fields for:
    - Event name
    - Event overview (short description)
    - Target attendees
    - Sponsorship value (cost, deliverables, etc.)
    - Contact information
- Submitted proposals are stored in the database and associated with the relevant sponsor.

### **3. User Authentication**
- **Login and Registration:** Authenticate users to access features.
- **Preloaded Test User with Sponsors:**
  - Username: `mock2`
  - Password: `mock`
- **Preloaded Test User with Events:**
  - Username: `mock`
  - Password: `mock`


## Example User Flow

- Log in as a user or register a user
- Create an Event
- View sponsors
- Select a sponsor and create a proposal for that sponsor
- View Proposals and you can see your outbound proposal
- Log in as mock2 (owns all sponsors)
- View proposals and you can see inbound proposals which you may accept or reject
    - Future iterations would have a messaging system here

There is no way in this demo to create sponsors as a user in this demonstration


## Tech Stack

### **Frontend**
- **Frameworks/Libraries:** Angular, Ionic
- **Styling:** SCSS
- **API Integration:** HTTPClient for communication with the backend.

### **Backend**
- **Framework:** Python FastAPI
- **Security:** JSON Web Tokens (JWT) for authentication and authorization.
- **Data Validation:** Pydantic for request validation.

### **Database**
- **Primary:** PostgreSQL for relational data storage.
- **Integration with SQLAlchemy:** ORM for database operations.

### **Cloud Deployment**
- **Platform:** Deployed using lightweight cloud solutions such as AWS or Vercel.

### **Other Tools**
- **Version Control:** Git
- **CI/CD:** Implemented for testing and deployment workflows.
- **Testing Frameworks:**
  - Frontend: Karma, Jasmine
  - Backend: Pytest

---
