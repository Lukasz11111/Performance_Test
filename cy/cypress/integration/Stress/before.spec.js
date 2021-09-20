describe('Before stresss test', () => {
  let domElements;
  beforeEach(function () {
    cy.loginToApm();
    cy.setDate('Last 1 month');
    cy.selectApmCard('Trace');
    cy.fixture('domelements').then((domelements) => {
      domElements = domelements;
    });
    cy.get('.rk-trace-t-tool > .grey').select('startTime');
    cy.wait(3000);
  });



   // Test case summary:
  // Expected result:
  it('Chcek recording count', () => {
    cy.get('.rk-trace-search > div:nth-of-type(1)').contains('Search').click();
    cy.readFile('stress.json').then((json) => {
      cy.get('.rk-page > :nth-child(4)').then((text) => {
        json.APM_Spans_Before = parseInt(text.text());
        cy.get(':nth-child(3) > .rk-trace-bar-i').click()
        cy.contains('Success').click()
        cy.get('.rk-trace-search-btn > span.vm').click()
        cy.wait(2000)
        cy.get('.rk-page > :nth-child(4)').then((text) => {
          json.APM_Successes_Before = parseInt(text.text());
          cy.get(':nth-child(3) > .rk-trace-bar-i').click()
          cy.contains('Error').click()
          cy.get('.rk-trace-search-btn > span.vm').click()
          cy.wait(2000)
          cy.get('.rk-page > :nth-child(4)').then((text) => {
            json.APM_Errors_Before = parseInt(text.text());
          });
        })
      });
      cy.loginToHome();
      cy.get('#applications-dropdown').click();
      // Go to the 'InvoiceJava' Application
      cy.get(`[title=${json.Application_name}]`).click();
      cy.get('#app-navigation > :nth-child(2) > .nav-link').click()
      cy.wait(3000)
      cy.contains("Last").then((text) => {
        let tex = new String(text.text())
        tex = tex.split(" ")[1].substring(1).slice(0, -1)
        json.Recording_Before = parseInt(tex);
      })
      cy.writeFile('stress.json', json)
    });
  });

});
