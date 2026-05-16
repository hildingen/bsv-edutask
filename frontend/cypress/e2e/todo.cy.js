describe('Test todo functionality', () => {
    // define variables that we need on multiple occasions
    let uid; // user id
    let name; // name of the user (firstName + ' ' + lastName)
    let email; // email of the user
    let task_id; // task id

    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user,
            }).then((response) => {
                uid = response.body._id.$oid;
                name = user.firstName + ' ' + user.lastName;
                email = user.email;
            });
        });

        // create a fabricated task from a fixture
        cy.fixture('task.json').then((task) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/tasks/create',
                form: true,
                body: { ...task, userid: uid },
            }).then((response) => {
                task_id = response.body[0]._id.$oid;
            });
        });
    });

    beforeEach(function () {
        cy.viewport(1280, 720);
        // enter the main main page
        cy.visit('http://localhost:3000');

        // Sign in user
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email);

        // Sign in user
        cy.get('form').submit();

        // Click on first task
        cy.get('.container-element').find('a').click();
    });

    it('create a new todo', () => {
        // Find input and click
        cy.get('input[placeholder="Add a new todo item"]')
            .scrollIntoView()
            .click();

        // Find input and type First todo and click enter
        cy.get('input[placeholder="Add a new todo item"]').type(
            'New todo item{enter}'
        );

        // Find the todo item list and confirm there is two elements since we have one at start
        cy.get('.todo-item')
            .find('span.editable')
            .should('have.text', 'New todo item');
    });

    it('create button disabled', () => {
        cy.get('input[value="Add"]').should('be.disabled');
    });

    it('check a todo item', () => {
        cy.get('.todo-item')
            .find('span.checker')
            .should('have.class', 'unchecked');
        cy.get('.todo-item').find('span.checker').click();
        cy.get('.todo-item')
            .find('span.checker')
            .should('have.class', 'checked');
    });

    it('uncheck a todo item', () => {
        cy.get('.todo-item')
            .find('span.checker')
            .should('have.class', 'checked');
        cy.get('.todo-item').find('span.checker').click();
        cy.get('.todo-item')
            .find('span.checker')
            .should('have.class', 'unchecked');
    });

    it('delete todo item', () => {
        cy.get('.todo-item').should('have.length', 1);
        cy.get('.todo-item').find('span.remover').click();
        cy.get('.todo-item').should('not.exist');
    });

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`,
        }).then((response) => {
            cy.log(response.body);
        });

        // Clean up task
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/tasks/byid/${uid}`,
        }).then((response) => {
            cy.log(response.body);
        });
    });
});
