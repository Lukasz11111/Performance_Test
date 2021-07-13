
import { UrlHelper, QueryHelper } from '../support/helpers';

var demoUrlHelper = new UrlHelper(Cypress.env('RDB_HOSTNAME'), 'http://');

// Purpose of the command: To login directly to apm page
Cypress.Commands.add('loginToApm', () => {
    // Visit apm start page. Value is saved in enviromental variable
    cy.visit(demoUrlHelper.getFullUrl(Cypress.env('APM_START_PAGE')));
    cy.fixture('domelements').then((domElements) => {
      // Type login and password
      cy.get(domElements.email).type(Cypress.env('LOGIN'));
      cy.get(domElements.password).type(Cypress.env('PASSWORD'));
  
      // Click login button
      cy.get(domElements.loginButton).click();
    });
  });

// Purpose of the command: Allows to select card from header
Cypress.Commands.add('selectApmCard', (cardName) => {
    cy.fixture('domelements').then((domElements) => {
      cy.get('.rk-header').contains(cardName).click();
    });
  });

  // Purpose of the command: To login directly to monitor page
Cypress.Commands.add('loginToHome', () => {
    cy.visit(demoUrlHelper.getFullUrl(Cypress.env('HOME_START_PAGE')));
  });

// Purpose of the command: Set main date on page
Cypress.Commands.add('setDate', (date) => {
    cy.get('.datepicker > .cp').click();
    cy.contains(date).click();
  });
  // Purpose of the command: Set date in trace
  Cypress.Commands.add('setDateTrace', (date) => {
    // Select datepicker from trace
    cy.get(':nth-child(3) > .datepicker > .cp').click();
    // Select wanted value
    cy.contains(date).click();
  });

//Check if all traces have been received
Cypress.Commands.add('getTrace', (k) => {
    cy.get('.flex-h.rk-page > span:nth-of-type(2)').then((text) => {
        cy.wait(10000);
        cy.reload();
        cy.get('.rk-header > :nth-child(2) > :nth-child(4)').click();
        cy.get('.rk-trace-search > div:nth-of-type(1)').contains('Search').click();
        cy.wait(5000);
        cy.get('.flex-h.rk-page > span:nth-of-type(2)').then((text_aftre) => {
            if (parseInt(text.text()) != parseInt(text_aftre.text())) {
                cy.get('fail');
            }
        });
    });
});

//Check if all traces have been received
Cypress.Commands.add('getRecordings', () => {
    cy.contains('Last').then((text) => {
        let tex = new String(text.text());
        tex = tex.split(' ')[1].substring(1).slice(0, -1);
        let recordin_count = parseInt(tex);
        cy.wait(10000);
        cy.reload();
        cy.wait(5000);
        cy.contains('Last').then((text_after) => {
            let tex_after = new String(text_after.text());
            tex_after = tex_after.split(' ')[1].substring(1).slice(0, -1);
            let recordin_count_after = parseInt(tex_after);
            if (recordin_count_after != recordin_count) {
                cy.get('fail');
            }
        });
    });
});