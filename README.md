# train-ticket-booking

Build a Back end train booking system

Roles -> 
1. Admin
2. User

Assumptions
1. There will be 60 seats in A/C Sleeper
2. There will be 60 seats in Non A/C Sleeper
3. There will be 120 seats in Seater

Operations

Admin can do the following:
* Add additional coaches to the train
* View all seats in a coach / train
* Remove the coaches of a train
* Update the details of the coaches in a train
  
 Users can do the following:
	
 * Book seats of a specific coach in a train
 * View the available seats in a coach
 * Book multiple seats
 * A user cannot book a seat or seats if it is not available or booked by anyone.
 * An API to fetch all available seats
 * An API to fetch all booked seats
