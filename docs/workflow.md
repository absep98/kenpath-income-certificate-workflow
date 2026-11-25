# Income Certificate Workflow

> Status: DRAFT. Items marked **(verified)** come from the official Nadakacheri portal.
> Items marked **(assumption)** are a best guess from general knowledge and must be checked
> with a real applicant or officer before the README states them as fact.

## 1. Problem

**Who uses this system?**
Village Accountants (VA) and Revenue Inspectors (RI) who verify applications in the field, and the
Tahsildar who issues the final certificate. **(verified: VA and RI do field verification, via the
Samyojane mobile app since 2019. Tahsildar as final authority is an assumption.)**

**What problem are we solving?**
Income certificates are needed for scholarships, fee concessions and welfare schemes. Applications
arrive digitally, but officers still check documents by hand, work out which cases are urgent by
memory, and write rejection reasons from scratch. Applications sit idle at a stage because nothing
tells the officer what to look at first. The citizen sees "pending" with no reason.
**(assumption)** The tool aims to cut review time per case and give a clear reason on every return.

## 2. Workflow stages

### Stage 1: Application Intake
Officer: system, plus Village Accountant picks it up (assumption)
Responsibilities: confirm the application is complete and assign it to the right VA by village.
Documents checked: identity proof, address proof, income declaration or affidavit, photo (assumption).
Possible actions: forward to Field Verification, or return to citizen if documents are missing.
**AI helps:** flag missing or unreadable documents.

### Stage 2: Field Verification
Officer: Village Accountant (VA) **(verified role)**
Responsibilities: verify the applicant lives there and the declared income is plausible, on the ground.
Documents checked: residence, family details, income declaration.
Possible actions: forward to RI Review, return for correction, or reject with a reason.
**AI helps:** compare the declared income with the occupation and family size and flag inconsistencies.
The VA decides.

### Stage 3: Revenue Inspector Review
Officer: Revenue Inspector (RI) **(verified role)**
Responsibilities: cross-check the VA's report and the documents, and confirm the case is consistent.
Documents checked: VA report plus original documents.
Possible actions: forward to Final Decision, return to VA, or reject with a reason.
**AI helps:** summarise the whole case in plain Kannada so the RI reads one paragraph first.

### Stage 4: Final Decision
Officer: Tahsildar **(assumption: final issuing authority)**
Responsibilities: approve and issue, reject, or send back.
Documents checked: the RI's recommendation and the case summary.
Possible actions: Approve, Reject, or Return (to RI or VA).
**AI helps:** draft the reason text for the decision. The officer edits it and clicks the button.

## 3. Common delays

1. Missing or wrong documents found late, at the field stage, instead of at intake. **(assumption)**
2. Officers have no view of which cases are oldest or close to the deadline, so they work in arrival
   order. **(assumption)**
3. Rejections and returns carry vague reasons, so citizens reapply and the cycle repeats. **(assumption)**

## 4. Sources

- https://nadakacheri.karnataka.gov.in/ajsk (official portal, field verification by RI and VA)
- https://www.indiafilings.com/learn/nadakacheri-income-caste-certificate-karnataka/ (general overview, not official)
- Not yet confirmed: fee, timeline, exact officer chain. Check before submission.
