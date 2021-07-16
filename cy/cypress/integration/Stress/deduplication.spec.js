describe('After stresss test', () => {
  let domElements;
  beforeEach(function () {
    cy.loginToApm();
    cy.fixture('domelements').then((domelements) => {
      domElements = domelements;
    });
  });

  // Test case summary:
  // Expected result:
  it('Chcek recording count', () => {
  cy.visit(Cypress.env("RDB_HOSTNAME") +'/globalSettings/Index')
  cy.contains('Recording Options').click()
  cy.get('#on-event-deduplication').then((checkbox)=>{
      if(checkbox[0].checked){
        cy.get('#on-event-deduplication').click()
    }
  })
    
    cy.get('#recording-options-content > .card-body > .btn-ghost').click()
  });
});
