# S1-D interval certificates (T16, T17)

Generated 2026-09-06 00:32:25; Python 3.12.13, mpmath 1.4.1 (preserved seed result: mpmath 1.3.0, 50 digits).

Seed copy sha256 085b0f10c20a1b7d48125ba0480c1dde5968958005287f9325ef0ce6897b8194 (identical before and after the run; run under `run_seed.sh`, which refuses PYTHONOPTIMIZE and -O).

186 checks, 0 failures.

## r = 1.55, v in [0.46031618, 0.46031620]

| attempt | digits | mesh | accepted | failures |
|---|---:|---:|---|---|
| 1 | 50 | 200 | True | - |
| 2 | 50 | 400 | True | - |

- Psi(v_-) in [0.0000000001140624141656750761..., 0.0000000001140624141656750761...]
- Psi(v_+) in [-0.000000000096243882594929088..., -0.000000000096243882594929088...]
- Gamma_H lower 0.00007617774207723405691...; L_U upper 0.121975806451612903...
- E in [0.54505288980894571352..., 0.54505289213224668974...]
- pooling margin lower 0.007802419354838709...

## r = 1.60, v in [0.70747537, 0.70747539]

| attempt | digits | mesh | accepted | failures |
|---|---:|---:|---|---|
| 1 | 50 | 200 | True | - |
| 2 | 50 | 400 | True | - |

- Psi(v_-) in [0.0000000001236570290324983567..., 0.0000000001236570290324983567...]
- Psi(v_+) in [-0.000000000121297872728709390..., -0.000000000121297872728709390...]
- Gamma_H lower 0.00275319485548009161736...; L_U upper 0.140625000000000000...
- E in [0.54875630627940255309..., 0.54875630846126992728...]
- pooling margin lower 0.005937499999999999...

## r = 1.65, v in [0.90333198, 0.90333201]

| attempt | digits | mesh | accepted | failures |
|---|---:|---:|---|---|
| 1 | 50 | 200 | True | - |
| 2 | 50 | 400 | True | - |

- Psi(v_-) in [0.0000000001725944272176983539..., 0.0000000001725944272176983539...]
- Psi(v_+) in [-0.000000000242932975998864511..., -0.000000000242932975998864511...]
- Gamma_H lower 0.00549217673164317566152...; L_U upper 0.160037878787878787...
- E in [0.55136079885677678853..., 0.55136080197006227459...]
- pooling margin lower 0.003996212121212121...

## Checks

| status | check | note |
|---|---|---|
| pass | seed copy byte-identical to verification/certify_asymmetric.py | 085b0f10c20a1b7d48125ba0480c1dde5968958005287f9325ef0ce6897b8194 |
| pass | seed copy unchanged after run (sha256_after_run.txt) |  |
| pass | seed run completed with assertions enabled |  |
| pass | seed r=1.55 FOC_at_left: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 FOC_at_right: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 high_global_derivative_lower: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 derivative_Lipschitz_bound: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 pooling_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 low_cost_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 high_cost_prior_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 entry: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 low_trader_payoff: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 high_trader_payoff: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.55 high_derivative_mesh_min_lower identical |  |
| pass | seed r=1.6 FOC_at_left: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 FOC_at_right: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 high_global_derivative_lower: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 derivative_Lipschitz_bound: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 pooling_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 low_cost_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 high_cost_prior_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 entry: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 low_trader_payoff: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 high_trader_payoff: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.6 high_derivative_mesh_min_lower identical |  |
| pass | seed r=1.65 FOC_at_left: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 FOC_at_right: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 high_global_derivative_lower: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 derivative_Lipschitz_bound: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 pooling_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 low_cost_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 high_cost_prior_margin: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 entry: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 low_trader_payoff: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 high_trader_payoff: fresh run reproduces preserved enclosure (identical string) |  |
| pass | seed r=1.65 high_derivative_mesh_min_lower identical |  |
| pass | r=1.55: declared bracket matches numerics.params and C.2 |  |
| pass | r=1.55: accepted at the declared precision/mesh (50 digits, 200 intervals) | accepted at 50 digits, 200 intervals |
| pass | r=1.55: declared refinement (400 intervals) also accepted |  |
| pass | r=1.55 [1] support p < ell < r < h |  |
| pass | r=1.55 [1] prior high-cost exclusion c_H - B_r(1/2) > 0 | 1.30685483870967741935483870967741935483870967741933731916809 |
| pass | r=1.55 [1] low-cost participation B_r(m) - c_L > 0 | 1.63616479879304527253746220123286239297029703001444742226734 |
| pass | r=1.55 [2] threshold 1/2 < tau < M_v and -v < x* < 1 throughout the bracket | tau=('0.646797717184527584020291693088142041851616994292957010673498', '0.646797717184527584020291693088142041851616994292963692585274'), M_v=('0.67483996338587 |
| pass | r=1.55 [3] Psi(r, v_-) outward enclosure strictly positive | ('0.000000000114062414165675076111843508386085921009670420769256224721302', '0.000000000114062414165675076111843508386085921009672049485251437153025') |
| pass | r=1.55 [4] Psi(r, v_+) outward enclosure strictly negative | ('-0.0000000000962438825949290881135393632204851109516504962911206049691332', '-0.0000000000962438825949290881135393632204851109516488675751253925374112') |
| pass | r=1.55 [5] low-type strict concavity (OA.60: b > 1/2; posterior nondecreasing since 1 > -v; e nondecreasing) |  |
| pass | r=1.55 [6] high-type derivative enclosed on every mesh point with v = [v_-, v_+] interval (source inspection) and Gamma_H > 0 | Gamma_H=('0.0000761777420772340569143373986259299876197330859673641024805815', '0.0000761777420772340569143373986259299876197330859673699752546028'), mesh min l |
| pass | r=1.55 [6] L_U = 2 Delta/b + Delta/b^2 reproduced |  |
| pass | r=1.55 [7] pooling-existence margin k - rho Delta/2 > 0 | 0.00780241935483870967741935483870967741935483870967732184742453 |
| pass | r=1.55 certificates.csv Psi_left_lower equals port endpoint string | csv=0.000000000114062414165675076111843508386085921009670420769256224721302 port=0.000000000114062414165675076111843508386085921009670420769256224721302 |
| pass | r=1.55 certificates.csv Psi_left_upper equals port endpoint string | csv=0.000000000114062414165675076111843508386085921009672049485251437153025 port=0.000000000114062414165675076111843508386085921009672049485251437153025 |
| pass | r=1.55 certificates.csv Psi_right_lower equals port endpoint string | csv=-0.0000000000962438825949290881135393632204851109516504962911206049691332 port=-0.0000000000962438825949290881135393632204851109516504962911206049691332 |
| pass | r=1.55 certificates.csv Psi_right_upper equals port endpoint string | csv=-0.0000000000962438825949290881135393632204851109516488675751253925374112 port=-0.0000000000962438825949290881135393632204851109516488675751253925374112 |
| pass | r=1.55 certificates.csv Gamma_H_lower equals port endpoint string | csv=0.0000761777420772340569143373986259299876197330859673641024805815 port=0.0000761777420772340569143373986259299876197330859673641024805815 |
| pass | r=1.55 certificates.csv L_U_upper equals port endpoint string | csv=0.121975806451612903225806451612903225806451612903226539306453 port=0.121975806451612903225806451612903225806451612903226539306453 |
| pass | r=1.55 certificates.csv E_lower equals port endpoint string | csv=0.545052889808945713520237620328749119481683845800618298332444 port=0.545052889808945713520237620328749119481683845800618298332444 |
| pass | r=1.55 certificates.csv E_upper equals port endpoint string | csv=0.545052892132246689741896675903819707329977318624990770537445 port=0.545052892132246689741896675903819707329977318624990770537445 |
| pass | r=1.55 certificates.csv pooling_margin_lower equals port endpoint string | csv=0.00780241935483870967741935483870967741935483870967732184742453 port=0.00780241935483870967741935483870967741935483870967732184742453 |
| pass | r=1.55 certificates.csv threshold_margin_lower equals port endpoint string | csv=1.63616479879304527253746220123286239297029703001444742226734 port=1.63616479879304527253746220123286239297029703001444742226734 |
| pass | r=1.55 certificates.csv mesh/digits/accepted |  |
| pass | r=1.55 port vs seed FOC_at_left (full endpoints, 1e-45) | seed=[1.140624141656750761118435083860859210096704207692562247E-10,1.140624141656750761118435083860859210096720494852514372E-10] port=[1.14062414165675076111843 |
| pass | r=1.55 port vs seed FOC_at_right (full endpoints, 1e-45) | seed=[-9.624388259492908811353936322048511095165049629112060497E-11,-9.624388259492908811353936322048511095164886757512539254E-11] port=[-9.62438825949290881135 |
| pass | r=1.55 port vs seed high_global_derivative_lower (full endpoints, 1e-45) | seed=[0.00007617774207723405691433739862592998761973308596736410248,0.00007617774207723405691433739862592998761973308596736997525] port=[0.000076177742077234056 |
| pass | r=1.55 port vs seed derivative_Lipschitz_bound (full endpoints, 1e-45) | seed=[0.1219758064516129032258064516129032258064516129032245347,0.1219758064516129032258064516129032258064516129032265393] port=[0.12197580645161290322580645161 |
| pass | r=1.55 port vs seed pooling_margin (full endpoints, 1e-45) | seed=[0.007802419354838709677419354838709677419354838709677321847,0.007802419354838709677419354838709677419354838709677551538] port=[0.0078024193548387096774193 |
| pass | r=1.55 port vs seed low_cost_margin (full endpoints, 1e-45) | seed=[1.636164798793045272537462201232862392970297030014447422,1.636164798793045272537462201232862392970297030014495532] port=[1.6361647987930452725374622012328 |
| pass | r=1.55 port vs seed high_cost_prior_margin (full endpoints, 1e-45) | seed=[1.306854838709677419354838709677419354838709677419337319,1.306854838709677419354838709677419354838709677419369392] port=[1.3068548387096774193548387096774 |
| pass | r=1.55 port vs seed entry (full endpoints, 1e-45) | seed=[0.5450528898089457135202376203287491194816838458006182983,0.5450528921322466897418966759038197073299773186249907705] port=[0.54505288980894571352023762032 |
| pass | r=1.55 port vs seed low_trader_payoff (full endpoints, 1e-45) | seed=[0.00166075006024715300243394311964166115300876407143712572,0.001660750461131846383170625668484142530207749289754819477] port=[0.00166075006024715300243394 |
| pass | r=1.55 port vs seed high_trader_payoff (full endpoints, 1e-45) | seed=[0.003607846469803457242795166727209707442925333772460392698,0.003607846989466334871742291717746158164322737607175869478] port=[0.0036078464698034572427951 |
| pass | r=1.55 independent 30-digit quadrature: Psi(v_-) > 0 and within 1e-22 of the port enclosure | Psi(v_-)=1.1406241416567507611e-10, distance to enclosure 4.8e-33 |
| pass | r=1.55 independent 30-digit quadrature: Psi(v_+) < 0 and within 1e-22 of the port enclosure | Psi(v_+)=-9.6243882594929088114e-11, distance to enclosure 2.5e-33 |
| pass | r=1.55 independent quadrature: min_j U_H'(s_j) over v in {v_-, mid, v_+} >= port mesh minimum lower endpoint | independent min 0.000381117891391955 at (v, j)=('0.46031620', 0); port lower 0.000381117258206266314978853527658188052135862118225430737860110 |
| pass | r=1.55 independent quadrature: min_j U_H'(s_j) - L_U/(2n) > 0 |  |
| pass | r=1.55 independent entry E(v) at v_-, mid, v_+ inside the port enclosure | E=['0.545052890770728', '0.545052890970596', '0.545052891170464']; enclosure [0.545052889808945713520237620328749119481683845800618298332444, 0.5450528921322466 |
| pass | T17 r=1.55 registry entry display lower is floor(E_lower, 10 dp) | 0.5450528898 vs 0.545052889808945713520237620328749119481683845800618298332444 |
| pass | T17 r=1.55 registry entry display upper is ceil(E_upper, 10 dp) | 0.5450528922 vs 0.545052892132246689741896675903819707329977318624990770537445 |
| pass | T17 r=1.55 registry entry lower/upper columns equal port endpoints |  |
| pass | T17 r=1.55 registry v display equals the exact declared bracket | [0.46031618,0.46031620] |
| pass | T17 r=1.55 registry Gamma_H display is floor(lower, 10 dp) | 0.0000761777 vs 0.0000761777420772340569143373986259299876197330859673641024805815 |
| pass | T17 r=1.55 registry Psi_left display rounds the lower endpoint down (12 dp) and stays positive | 1.14E-10 |
| pass | T17 r=1.55 registry Psi_right display rounds the upper endpoint up (12 dp) and stays negative | -9.6E-11 |
| pass | T17 r=1.55 main_filled.md table row shows the exact bracket and the outward entry display | 1.55&[0.46031618,\,0.46031620]&[0.5450528898,\,0.5450528922] |
| pass | T17 r=1.55 main_filled.md shows the Gamma_H display |  |
| pass | T17 r=1.55 main_filled.md shows the Psi displays | 0.000000000114 / -0.000000000096 |
| pass | r=1.60: declared bracket matches numerics.params and C.2 |  |
| pass | r=1.60: accepted at the declared precision/mesh (50 digits, 200 intervals) | accepted at 50 digits, 200 intervals |
| pass | r=1.60: declared refinement (400 intervals) also accepted |  |
| pass | r=1.60 [1] support p < ell < r < h |  |
| pass | r=1.60 [1] prior high-cost exclusion c_H - B_r(1/2) > 0 | 1.32187499999999999999999999999999999999999999999997220324701 |
| pass | r=1.60 [1] low-cost participation B_r(m) - c_L > 0 | 1.62459188242583163565532223830843011157977701053302953207982 |
| pass | r=1.60 [2] threshold 1/2 < tau < M_v and -v < x* < 1 throughout the bracket | tau=('0.648734177215189873417721518987341772151898734177209269192097', '0.648734177215189873417721518987341772151898734177221296633294'), M_v=('0.70135061895119 |
| pass | r=1.60 [3] Psi(r, v_-) outward enclosure strictly positive | ('0.000000000123657029032498356765117067551683707823712780098275612805589', '0.000000000123657029032498356765117067551683707823715077005448348286223') |
| pass | r=1.60 [4] Psi(r, v_+) outward enclosure strictly negative | ('-0.000000000121297872728709390965226244061214620982137720484230956445175', '-0.000000000121297872728709390965226244061214620982135465339006816155098') |
| pass | r=1.60 [5] low-type strict concavity (OA.60: b > 1/2; posterior nondecreasing since 1 > -v; e nondecreasing) |  |
| pass | r=1.60 [6] high-type derivative enclosed on every mesh point with v = [v_-, v_+] interval (source inspection) and Gamma_H > 0 | Gamma_H=('0.00275319485548009161736182814890494783449160744670037037017392', '0.00275319485548009161736182814890494783449160744670038081066108'), mesh min lower |
| pass | r=1.60 [6] L_U = 2 Delta/b + Delta/b^2 reproduced |  |
| pass | r=1.60 [7] pooling-existence margin k - rho Delta/2 > 0 | 0.00593749999999999999999999999999999999999999999999988390178290 |
| pass | r=1.60 certificates.csv Psi_left_lower equals port endpoint string | csv=0.000000000123657029032498356765117067551683707823712780098275612805589 port=0.000000000123657029032498356765117067551683707823712780098275612805589 |
| pass | r=1.60 certificates.csv Psi_left_upper equals port endpoint string | csv=0.000000000123657029032498356765117067551683707823715077005448348286223 port=0.000000000123657029032498356765117067551683707823715077005448348286223 |
| pass | r=1.60 certificates.csv Psi_right_lower equals port endpoint string | csv=-0.000000000121297872728709390965226244061214620982137720484230956445175 port=-0.000000000121297872728709390965226244061214620982137720484230956445175 |
| pass | r=1.60 certificates.csv Psi_right_upper equals port endpoint string | csv=-0.000000000121297872728709390965226244061214620982135465339006816155098 port=-0.000000000121297872728709390965226244061214620982135465339006816155098 |
| pass | r=1.60 certificates.csv Gamma_H_lower equals port endpoint string | csv=0.00275319485548009161736182814890494783449160744670037037017392 port=0.00275319485548009161736182814890494783449160744670037037017392 |
| pass | r=1.60 certificates.csv L_U_upper equals port endpoint string | csv=0.140625000000000000000000000000000000000000000000001002286767 port=0.140625000000000000000000000000000000000000000000001002286767 |
| pass | r=1.60 certificates.csv E_lower equals port endpoint string | csv=0.548756306279402553094473342650650704987833563703042353794586 port=0.548756306279402553094473342650650704987833563703042353794586 |
| pass | r=1.60 certificates.csv E_upper equals port endpoint string | csv=0.548756308461269927283787391337035286049034141128488454660113 port=0.548756308461269927283787391337035286049034141128488454660113 |
| pass | r=1.60 certificates.csv pooling_margin_lower equals port endpoint string | csv=0.00593749999999999999999999999999999999999999999999988390178290 port=0.00593749999999999999999999999999999999999999999999988390178290 |
| pass | r=1.60 certificates.csv threshold_margin_lower equals port endpoint string | csv=1.62459188242583163565532223830843011157977701053302953207982 port=1.62459188242583163565532223830843011157977701053302953207982 |
| pass | r=1.60 certificates.csv mesh/digits/accepted |  |
| pass | r=1.60 port vs seed FOC_at_left (full endpoints, 1e-45) | seed=[1.236570290324983567651170675516837078237127800982756128E-10,1.236570290324983567651170675516837078237150770054483483E-10] port=[1.23657029032498356765117 |
| pass | r=1.60 port vs seed FOC_at_right (full endpoints, 1e-45) | seed=[-1.212978727287093909652262440612146209821377204842309564E-10,-1.212978727287093909652262440612146209821354653390068162E-10] port=[-1.21297872728709390965 |
| pass | r=1.60 port vs seed high_global_derivative_lower (full endpoints, 1e-45) | seed=[0.00275319485548009161736182814890494783449160744670037037,0.002753194855480091617361828148904947834491607446700380811] port=[0.00275319485548009161736182 |
| pass | r=1.60 port vs seed derivative_Lipschitz_bound (full endpoints, 1e-45) | seed=[0.1406249999999999999999999999999999999999999999999986636,0.1406250000000000000000000000000000000000000000000010023] port=[0.14062499999999999999999999999 |
| pass | r=1.60 port vs seed pooling_margin (full endpoints, 1e-45) | seed=[0.005937499999999999999999999999999999999999999999999883902,0.005937500000000000000000000000000000000000000000000134473] port=[0.0059374999999999999999999 |
| pass | r=1.60 port vs seed low_cost_margin (full endpoints, 1e-45) | seed=[1.624591882425831635655322238308430111579777010533029532,1.624591882425831635655322238308430111579777010533088333] port=[1.6245918824258316356553222383084 |
| pass | r=1.60 port vs seed high_cost_prior_margin (full endpoints, 1e-45) | seed=[1.321874999999999999999999999999999999999999999999972203,1.321875000000000000000000000000000000000000000000025659] port=[1.3218749999999999999999999999999 |
| pass | r=1.60 port vs seed entry (full endpoints, 1e-45) | seed=[0.5487563062794025530944733426506507049878335637030423538,0.5487563084612699272837873913370352860490341411284884547] port=[0.54875630627940255309447334265 |
| pass | r=1.60 port vs seed low_trader_payoff (full endpoints, 1e-45) | seed=[0.00449220944473735899370103747013246791557506877675347921,0.004492210122069181110304489904685808931668520039630409556] port=[0.00449220944473735899370103 |
| pass | r=1.60 port vs seed high_trader_payoff (full endpoints, 1e-45) | seed=[0.006349633797142939659574576267637934358766280184361610221,0.006349634362275597377502055644047344499192034132820750134] port=[0.0063496337971429396595745 |
| pass | r=1.60 independent 30-digit quadrature: Psi(v_-) > 0 and within 1e-22 of the port enclosure | Psi(v_-)=1.2365702903249835677e-10, distance to enclosure 6.6e-33 |
| pass | r=1.60 independent 30-digit quadrature: Psi(v_+) < 0 and within 1e-22 of the port enclosure | Psi(v_+)=-1.2129787272870939097e-10, distance to enclosure 7.8e-33 |
| pass | r=1.60 independent quadrature: min_j U_H'(s_j) over v in {v_-, mid, v_+} >= port mesh minimum lower endpoint | independent min 0.00310475809978466 at (v, j)=('0.70747539', 0); port lower 0.00310475735548009161736182814890494783449160744670037517279801 |
| pass | r=1.60 independent quadrature: min_j U_H'(s_j) - L_U/(2n) > 0 |  |
| pass | r=1.60 independent entry E(v) at v_-, mid, v_+ inside the port enclosure | E=['0.548756307179727', '0.548756307370336', '0.548756307560945']; enclosure [0.548756306279402553094473342650650704987833563703042353794586, 0.5487563084612699 |
| pass | T17 r=1.60 registry entry display lower is floor(E_lower, 10 dp) | 0.5487563062 vs 0.548756306279402553094473342650650704987833563703042353794586 |
| pass | T17 r=1.60 registry entry display upper is ceil(E_upper, 10 dp) | 0.5487563085 vs 0.548756308461269927283787391337035286049034141128488454660113 |
| pass | T17 r=1.60 registry entry lower/upper columns equal port endpoints |  |
| pass | T17 r=1.60 registry v display equals the exact declared bracket | [0.70747537,0.70747539] |
| pass | T17 r=1.60 registry Gamma_H display is floor(lower, 10 dp) | 0.0027531948 vs 0.00275319485548009161736182814890494783449160744670037037017392 |
| pass | T17 r=1.60 registry Psi_left display rounds the lower endpoint down (12 dp) and stays positive | 1.23E-10 |
| pass | T17 r=1.60 registry Psi_right display rounds the upper endpoint up (12 dp) and stays negative | -1.21E-10 |
| pass | T17 r=1.60 main_filled.md table row shows the exact bracket and the outward entry display | 1.60&[0.70747537,\,0.70747539]&[0.5487563062,\,0.5487563085] |
| pass | T17 r=1.60 main_filled.md shows the Gamma_H display |  |
| pass | T17 r=1.60 main_filled.md shows the Psi displays | 0.000000000123 / -0.000000000121 |
| pass | r=1.65: declared bracket matches numerics.params and C.2 |  |
| pass | r=1.65: accepted at the declared precision/mesh (50 digits, 200 intervals) | accepted at 50 digits, 200 intervals |
| pass | r=1.65: declared refinement (400 intervals) also accepted |  |
| pass | r=1.65 [1] support p < ell < r < h |  |
| pass | r=1.65 [1] prior high-cost exclusion c_H - B_r(1/2) > 0 | 1.33674242424242424242424242424242424242424242424240765508446 |
| pass | r=1.65 [1] low-cost participation B_r(m) - c_L > 0 | 1.61331286792728246900732887804884499311347812047499294730489 |
| pass | r=1.65 [2] threshold 1/2 < tau < M_v and -v < x* < 1 throughout the bracket | tau=('0.650670309964990180172487405003842541200580650670307303294472', '0.650670309964990180172487405003842541200580650670313985206248'), M_v=('0.72145009861574 |
| pass | r=1.65 [3] Psi(r, v_-) outward enclosure strictly positive | ('0.000000000172594427217698353965312559861557874040549603347322385359729', '0.000000000172594427217698353965312559861557874040551774968649335268693') |
| pass | r=1.65 [4] Psi(r, v_+) outward enclosure strictly negative | ('-0.000000000242932975998864511564206395127313967436640454327639037518139', '-0.000000000242932975998864511564206395127313967436638240944363492418618') |
| pass | r=1.65 [5] low-type strict concavity (OA.60: b > 1/2; posterior nondecreasing since 1 > -v; e nondecreasing) |  |
| pass | r=1.65 [6] high-type derivative enclosed on every mesh point with v = [v_-, v_+] interval (source inspection) and Gamma_H > 0 | Gamma_H=('0.00549217673164317566152053893031536335808867529423702517633547', '0.00549217673164317566152053893031536335808867529423703561682263'), mesh min lower |
| pass | r=1.65 [6] L_U = 2 Delta/b + Delta/b^2 reproduced |  |
| pass | r=1.65 [7] pooling-existence margin k - rho Delta/2 > 0 | 0.00399621212121212121212121212121212121212121212121197613364281 |
| pass | r=1.65 certificates.csv Psi_left_lower equals port endpoint string | csv=0.000000000172594427217698353965312559861557874040549603347322385359729 port=0.000000000172594427217698353965312559861557874040549603347322385359729 |
| pass | r=1.65 certificates.csv Psi_left_upper equals port endpoint string | csv=0.000000000172594427217698353965312559861557874040551774968649335268693 port=0.000000000172594427217698353965312559861557874040551774968649335268693 |
| pass | r=1.65 certificates.csv Psi_right_lower equals port endpoint string | csv=-0.000000000242932975998864511564206395127313967436640454327639037518139 port=-0.000000000242932975998864511564206395127313967436640454327639037518139 |
| pass | r=1.65 certificates.csv Psi_right_upper equals port endpoint string | csv=-0.000000000242932975998864511564206395127313967436638240944363492418618 port=-0.000000000242932975998864511564206395127313967436638240944363492418618 |
| pass | r=1.65 certificates.csv Gamma_H_lower equals port endpoint string | csv=0.00549217673164317566152053893031536335808867529423702517633547 port=0.00549217673164317566152053893031536335808867529423702517633547 |
| pass | r=1.65 certificates.csv L_U_upper equals port endpoint string | csv=0.160037878787878787878787878787878787878787878787880205254013 port=0.160037878787878787878787878787878787878787878787880205254013 |
| pass | r=1.65 certificates.csv E_lower equals port endpoint string | csv=0.551360798856776788533769270145071166432320955743300255818651 port=0.551360798856776788533769270145071166432320955743300255818651 |
| pass | r=1.65 certificates.csv E_upper equals port endpoint string | csv=0.551360801970062274597481435420114471003452102733480241341781 port=0.551360801970062274597481435420114471003452102733480241341781 |
| pass | r=1.65 certificates.csv pooling_margin_lower equals port endpoint string | csv=0.00399621212121212121212121212121212121212121212121197613364281 port=0.00399621212121212121212121212121212121212121212121197613364281 |
| pass | r=1.65 certificates.csv threshold_margin_lower equals port endpoint string | csv=1.61331286792728246900732887804884499311347812047499294730489 port=1.61331286792728246900732887804884499311347812047499294730489 |
| pass | r=1.65 certificates.csv mesh/digits/accepted |  |
| pass | r=1.65 port vs seed FOC_at_left (full endpoints, 1e-45) | seed=[1.725944272176983539653125598615578740405496033473223854E-10,1.725944272176983539653125598615578740405517749686493353E-10] port=[1.72594427217698353965312 |
| pass | r=1.65 port vs seed FOC_at_right (full endpoints, 1e-45) | seed=[-2.429329759988645115642063951273139674366404543276390375E-10,-2.429329759988645115642063951273139674366382409443634924E-10] port=[-2.42932975998864511564 |
| pass | r=1.65 port vs seed high_global_derivative_lower (full endpoints, 1e-45) | seed=[0.005492176731643175661520538930315363358088675294237025176,0.005492176731643175661520538930315363358088675294237035617] port=[0.0054921767316431756615205 |
| pass | r=1.65 port vs seed derivative_Lipschitz_bound (full endpoints, 1e-45) | seed=[0.1600378787878787878787878787878787878787878787878778666,0.1600378787878787878787878787878787878787878787878802053] port=[0.16003787878787878787878787878 |
| pass | r=1.65 port vs seed pooling_margin (full endpoints, 1e-45) | seed=[0.003996212121212121212121212121212121212121212121211976134,0.003996212121212121212121212121212121212121212121212226705] port=[0.0039962121212121212121212 |
| pass | r=1.65 port vs seed low_cost_margin (full endpoints, 1e-45) | seed=[1.613312867927282469007328878048844993113478120474992947,1.613312867927282469007328878048844993113478120475035712] port=[1.6133128679272824690073288780488 |
| pass | r=1.65 port vs seed high_cost_prior_margin (full endpoints, 1e-45) | seed=[1.336742424242424242424242424242424242424242424242407655,1.336742424242424242424242424242424242424242424242439728] port=[1.3367424242424242424242424242424 |
| pass | r=1.65 port vs seed entry (full endpoints, 1e-45) | seed=[0.5513607988567767885337692701450711664323209557433002558,0.5513608019700622745974814354201144710034521027334802413] port=[0.55136079885677678853376927014 |
| pass | r=1.65 port vs seed low_trader_payoff (full endpoints, 1e-45) | seed=[0.008247599587712547112859719516319668722188572627147856146,0.008247601006578670205527502478860850295501837961891523573] port=[0.0082475995877125471128597 |
| pass | r=1.65 port vs seed high_trader_payoff (full endpoints, 1e-45) | seed=[0.009130197897942285631738106270226985667474283531770479877,0.009130198817322063329358126412829593776816596232614695181] port=[0.0091301978979422856317381 |
| pass | r=1.65 independent 30-digit quadrature: Psi(v_-) > 0 and within 1e-22 of the port enclosure | Psi(v_-)=1.7259442721769835397e-10, distance to enclosure 1.9e-32 |
| pass | r=1.65 independent 30-digit quadrature: Psi(v_+) < 0 and within 1e-22 of the port enclosure | Psi(v_+)=-2.4293297599886451156e-10, distance to enclosure 1.7e-32 |
| pass | r=1.65 independent quadrature: min_j U_H'(s_j) over v in {v_-, mid, v_+} >= port mesh minimum lower endpoint | independent min 0.00589227272055669 at (v, j)=('0.90333201', 0); port lower 0.00589227142861287263121750862728506032778564499120673028328485 |
| pass | r=1.65 independent quadrature: min_j U_H'(s_j) - L_U/(2n) > 0 |  |
| pass | r=1.65 independent entry E(v) at v_-, mid, v_+ inside the port enclosure | E=['0.551360800137273', '0.55136080041342', '0.551360800689567']; enclosure [0.551360798856776788533769270145071166432320955743300255818651, 0.55136080197006227 |
| pass | T17 r=1.65 registry entry display lower is floor(E_lower, 10 dp) | 0.5513607988 vs 0.551360798856776788533769270145071166432320955743300255818651 |
| pass | T17 r=1.65 registry entry display upper is ceil(E_upper, 10 dp) | 0.5513608020 vs 0.551360801970062274597481435420114471003452102733480241341781 |
| pass | T17 r=1.65 registry entry lower/upper columns equal port endpoints |  |
| pass | T17 r=1.65 registry v display equals the exact declared bracket | [0.90333198,0.90333201] |
| pass | T17 r=1.65 registry Gamma_H display is floor(lower, 10 dp) | 0.0054921767 vs 0.00549217673164317566152053893031536335808867529423702517633547 |
| pass | T17 r=1.65 registry Psi_left display rounds the lower endpoint down (12 dp) and stays positive | 1.72E-10 |
| pass | T17 r=1.65 registry Psi_right display rounds the upper endpoint up (12 dp) and stays negative | -2.42E-10 |
| pass | T17 r=1.65 main_filled.md table row shows the exact bracket and the outward entry display | 1.65&[0.90333198,\,0.90333201]&[0.5513607988,\,0.5513608020] |
| pass | T17 r=1.65 main_filled.md shows the Gamma_H display |  |
| pass | T17 r=1.65 main_filled.md shows the Psi displays | 0.000000000172 / -0.000000000242 |
| pass | [8] entry enclosures strictly ordered and non-overlapping across the three nodes | [('0.545052889808945713520237620328749119481683845800618298332444', '0.545052892132246689741896675903819707329977318624990770537445'), ('0.548756306279402553094 |
| pass | [8] displayed entry intervals strictly ordered and non-overlapping | [(Decimal('0.5450528898'), Decimal('0.5450528922')), (Decimal('0.5487563062'), Decimal('0.5487563085')), (Decimal('0.5513607988'), Decimal('0.5513608020'))] |
| pass | [8] port entry enclosures reproduce the seed's ordering assertion |  |
