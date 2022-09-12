# Observer Pattern

The Observer Pattern is a behavioral design pattern. It allows you to notify multiple objects about events that happen in your system, without tightly coupling them.

It describes how to you can create a dynamic subscription system with two types of objects; publishers and subscribers.

Use the Observer Pattern when changing the state of one object triggers other objects to also be updated. It's most useful when the set of objects to be updated is either unknown or changes dynamically. It can also be useful for reducing coupling and improving cohesion.

Conforms to the Open/Closed Principle and the Single Responsibility Principle.

### Pros:
- Single Responsibility Principle - Your functions can fulfil their main purpose without being aware of any follow-up actions.
- Open/Closed Principle - You can introduce new listeners without modifying your existing publishers.

### Cons:
- It's usually not possible to determine the order in which listeners will be called.
- It can be difficult to know which actions will be triggered by publishing an event.


## The example:
Imagine we have a web app that requires users to create an account. Once their account has been created, they will be emailed a one time verification code. Once registered, users can choose to upgrade their membership. When they upgrade, two things will happen; users will be emailed a receipt and the accounting department will be notified via Slack.

The functions will look like this:

Register:
- Create a user account
- Send verification email

Upgrade Account:
- Upgrade account plan
- Email receipt to user
- Notify accounting department via Slack

When looking at the above functions, what do you think about their cohesion?
Are there any issues with coupling?
Should the register action be responsible for both creating a user account and sending the verification email?
Should the upgrade action be responsible for upgrading an account's privileges, emailing a receipt, and notifying the accounting department?
What might happen if we change implementation details of the email/slack notification functions?

While performing these extra notification steps as part of our main flows will work, it might be better to extract them using the Observer Pattern. Let's see how the new flows would look.

Register:
- Create a user account
- Publish account creation

Upgrade Account:
- Upgrade account's plan
- Publish account upgrade

Now that our actions are publishing events, we need to build something to consume these events and handle subscribers. Let's take a look at how we can do this...

## Class Diagram:

![Class Diagram](./class_diagram.png?raw=true "Observer Pattern")