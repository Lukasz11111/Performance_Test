describe('After stresss test', () => {
  let domElements;
  beforeEach(function () {
    cy.loginToApm();
    cy.setDate('Last 1 month');
    cy.selectApmCard('Trace');
    cy.fixture('domelements').then((domelements) => {
      domElements = domelements;
    });
    cy.get('.rk-trace-t-tool > .grey').select('startTime');
    //cy.wait(5000);
  });

  // Test case summary:
  // Expected result:
  it('Chcek recording count', { retries: 10 }, () => {
    // console.log(Cypress.env('STRESS_APP_NAME'));
    cy.get('.rk-trace-search > div:nth-of-type(1)').contains('Search').click();
    cy.wait(2000);
    cy.log("before getTrace")
    cy.getTrace()
    cy.log("after getTrace")
    cy.readFile('stress.json').then((json) => {
      cy.get('.rk-page > :nth-child(4)').then((text) => {
        json.APM_Spans_After = parseInt(text.text());
        json.Trace_Span = (json.APM_Spans_After - json.APM_Spans_Before) * 15;
      });
      cy.log("after start read jeson")
      cy.loginToHome();
      cy.get('#applications-dropdown').click();
      cy.get(`[title=${json.Application_name}]`).click();

      cy.get('#app-navigation > :nth-child(2) > .nav-link').click();
      cy.getRecordings()
      cy.log("after get recording")
      cy.contains('Last').then((text) => {
        let tex = new String(text.text());
        tex = tex.split(' ')[1].substring(1).slice(0, -1);
        json.Recording_After = parseInt(tex);
        json.Recordings = (json.Recording_After - json.Recording_Before) * 10;

        cy.readFile(json.Jmeter_raport_path).then(
          (jsonFile) => {
            json.TotalJmeter.sampleCount = jsonFile.Total.sampleCount;
            json.TotalJmeter.meanResTime = jsonFile.Total.meanResTime;
            json.TotalJmeter.receivedKBytesPerSec =
              jsonFile.Total.receivedKBytesPerSec;
            json.TotalJmeter.sentKBytesPerSec = jsonFile.Total.sentKBytesPerSec;
            json.TotalJmeter.errorPct = jsonFile.Total.errorPct;

          }
        );
      });
      cy.writeFile('stress.json', json);
    });
  });
});
