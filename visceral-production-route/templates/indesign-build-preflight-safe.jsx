// The Visceral Theory of Sight - full 50-page InDesign layout builder
// Run from InDesign: File > Scripts > Other Script...
// Builds US Letter landscape facing pages, 3.175mm bleed, full-bleed section title pages with descriptions, multi-image spreads, captions, PDF, and audit report.

var ASSETS = [
  {
    "id": "A01",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-01-konly.jpg",
    "title": "a05-social-constraint-adobestock-1024472839",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A02",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-02-konly.jpg",
    "title": "a06-social-constraint-adobestock-1040196803",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A03",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-03-konly.jpg",
    "title": "a07-social-constraint-adobestock-1044937382",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A04",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-04-konly.jpg",
    "title": "a08-social-constraint-adobestock-1225023891",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A05",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-05-konly.jpg",
    "title": "a09-social-constraint-adobestock-140076283",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A06",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-06-konly.jpg",
    "title": "a10-social-constraint-adobestock-1462135790",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A07",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-07-konly.jpg",
    "title": "a11-social-constraint-adobestock-206067082",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A08",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-08-konly.jpg",
    "title": "a12-social-constraint-adobestock-268225510",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A09",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-09-konly.jpg",
    "title": "a13-social-constraint-adobestock-320500758",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A10",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-10-konly.jpg",
    "title": "a14-social-constraint-adobestock-368079012",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A11",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-11-konly.jpg",
    "title": "a15-social-constraint-adobestock-378198491",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A12",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-12-konly.jpg",
    "title": "a16-social-constraint-adobestock-565582008",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A13",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-13-konly.jpg",
    "title": "a17-social-constraint-adobestock-720156971",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A14",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-14-konly.jpg",
    "title": "a18-social-constraint-adobestock-730927617",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A15",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-15-konly.jpg",
    "title": "a19-social-constraint-adobestock-973721353",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A16",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-16-konly.jpg",
    "title": "a20-mediation-alex-bracken-l1sjo7tmvec-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A17",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-17-konly.jpg",
    "title": "a21-raw-agency-alexander-krivitskiy-az7rqwlwkhi-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A18",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-18-konly.jpg",
    "title": "a22-social-constraint-alexander-krivitskiy-gfopukdkmvo-uns",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A19",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-19-konly.jpg",
    "title": "a23-mediation-allef-vinicius-dkrntf-jgtw-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A20",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-20-konly.jpg",
    "title": "a24-raw-agency-amir-geshani-2jh8d3chnec-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A21",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-21-konly.jpg",
    "title": "a25-social-constraint-andrey-zvyagintsev-t8iknlqojcq-unspl",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A22",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-22-konly.jpg",
    "title": "a26-mediation-arielle-allouche-h82rqe4gria-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A23",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-23-konly.jpg",
    "title": "a27-raw-agency-baran-lotfollahi-lobgof8rurg-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A24",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-24-konly.jpg",
    "title": "a28-social-constraint-birmingham-museums-trust-oqpbewogd0o",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A25",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-25-konly.jpg",
    "title": "a29-mediation-boston-public-library-grbfmxpumu4-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A26",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-26-konly.jpg",
    "title": "a30-raw-agency-brunxs-monochrome-spniqdcpi9u-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A27",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-27-konly.jpg",
    "title": "a31-social-constraint-caleb-kastein-lmnz6-icim8-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A28",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-28-konly.jpg",
    "title": "a32-mediation-camila-quintero-franco-mc852jack1g-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A29",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-29-konly.jpg",
    "title": "a33-raw-agency-carl-cheng-o4l-vetcxhy-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A30",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-30-konly.jpg",
    "title": "a34-social-constraint-cole-keister-d6zqt8nfiq4-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A31",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-31-konly.jpg",
    "title": "a35-mediation-darius-bashar-3xegkkbinck-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A32",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-32-konly.jpg",
    "title": "a36-raw-agency-drew-dizzy-graham-ctkgzjtmjqu-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A33",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-33-konly.jpg",
    "title": "a37-social-constraint-elias-maurer-ssplu7ipc8g-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A34",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-34-konly.jpg",
    "title": "a38-mediation-elvis-kaiser-rqbk5ez6qa0-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A35",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-35-konly.jpg",
    "title": "a39-raw-agency-enesh-taganova-ioxgidqvqyq-unsplash-1",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A36",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-36-konly.jpg",
    "title": "a40-social-constraint-erik-mclean-gjtz5ckgeew-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A37",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-37-konly.jpg",
    "title": "a41-mediation-europeana-lbt8newonko-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A38",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-38-konly.jpg",
    "title": "a42-raw-agency-europeana-wwghncxmcqi-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A39",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-39-konly.jpg",
    "title": "a43-social-constraint-evilicio-inc-1hty8zlswls-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A40",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-40-konly.jpg",
    "title": "a44-mediation-flaviu-costin-vr-sbbcwklc-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A41",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-41-konly.jpg",
    "title": "a45-raw-agency-good-faces-r8vsytyy2oe-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A42",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-42-konly.jpg",
    "title": "a46-social-constraint-harry-quan-g1iycecw2ei-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A43",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-43-konly.jpg",
    "title": "a47-mediation-igor-rand-giw9ccl3hxa-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A44",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-44-konly.jpg",
    "title": "a48-raw-agency-ilya-mondryk-oceeo0ayn1s-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A45",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-45-konly.jpg",
    "title": "a49-social-constraint-janko-ferlic-brzt6bdt6na-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A46",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-46-konly.jpg",
    "title": "a50-mediation-jr-korpa-0lokelbdsbw-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A47",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-47-konly.jpg",
    "title": "a51-raw-agency-library-of-congress-v0jinhbf3xq-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A48",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-48-konly.jpg",
    "title": "a52-social-constraint-lorraine-hill-4dyxkga2gxa-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A49",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-49-konly.jpg",
    "title": "a53-mediation-mahdi-bafande-rw-azxeky7q-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A50",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-50-konly.jpg",
    "title": "a54-raw-agency-nastia-petruk-f-hajyv3wye-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A51",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-51-konly.jpg",
    "title": "a55-social-constraint-nina-zeynep-guler-fjjivsx-bxm-unspla",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A52",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-52-konly.jpg",
    "title": "a56-mediation-noah-buscher-11ldehfy-ha-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A53",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-53-konly.jpg",
    "title": "a57-raw-agency-ovie-ogege-6bwt4ci-ujs-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A54",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-54-konly.jpg",
    "title": "a58-social-constraint-see-plus-np3s9byoqac-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A55",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-55-konly.jpg",
    "title": "a59-mediation-smithsonian-elpq3w9epnk-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A56",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-56-konly.jpg",
    "title": "a60-raw-agency-smithsonian-otg-zz0tybe-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A57",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-57-konly.jpg",
    "title": "a61-social-constraint-teslariu-mihai-tk-szddiuis-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A58",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-58-konly.jpg",
    "title": "a62-mediation-the-new-york-public-library-ndjv4ntdf6g-unsp",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A59",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-59-konly.jpg",
    "title": "a63-raw-agency-toa-heftiba-fv1lunshcaw-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A60",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-60-konly.jpg",
    "title": "a64-social-constraint-umanoide-xjp9ak1oqhw-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A61",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-61-konly.jpg",
    "title": "a65-mediation-umesh-soni-hpklbuuel-k-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A62",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-62-konly.jpg",
    "title": "a67-social-constraint-zachary-kadolph-qbjgfnctwbu-unsplash",
    "group": "Group 3: Mediation"
  }
];
var OUTPUT_INDD = "/home/user/theory-of-sigh/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.indd";
var OUTPUT_IDML = "/home/user/theory-of-sigh/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.idml";
var OUTPUT_PDF = "/home/user/theory-of-sigh/visceral-production-route/output/pdf/the-visceral-theory-of-sight-50pp-indesign-auto.pdf";
var OUTPUT_REPORT = "/home/user/theory-of-sigh/visceral-production-route/reports/indesign-preflight-safe-build-report.json";

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

try {

var COPY = {
  "intro": "Sight is never only an act of seeing. It is a negotiation between the body that appears, the culture that disciplines appearance, and the surface that decides what the eye is allowed to touch. This issue moves through agency, constraint, and mediation as one continuous pressure system: the anatomy of looking, traced from the body outward to the veil.",
  "agency": "The body becomes the first instrument of authorship before it becomes a subject for interpretation. A hand, a shoulder, a mouth, a turned face: the figure enters as pressure, not as explanation. It claims the page by being present, and that presence unsettles the viewer who has not yet been handed a rule for reading it.\n\nThis is the oldest grammar of looking. In LeRoy McDermott's study of Upper Paleolithic female figurines, the strange proportions of the earliest carved bodies read not as another person's gaze but as self-representation, the body seen from within by the one who inhabits it.[1] Sight begins as ownership before it becomes display.\n\nA figure can be partial and still be active. A cropped body still claims space; a single eye still returns the look. So the opening pages stay close, image-led, and a little uncomfortable, letting presence arrive before permission. Looking here is not passive reception. The eye learns by pressure, repetition, and contrast, and a body seen across a sequence becomes a pattern the viewer is slowly trained to recognize. Before culture explains the figure, the figure has already insisted on being seen.",
  "constraint": "Culture turns visibility into a protocol. Bodily force is no longer allowed to stand alone; it is arranged by posture, costume, rank, ritual, maternity, and inherited rules of display. A face still looks outward, but now it looks through an architecture of expectation.\n\nElizabeth Mulley's study of Laura Muntz gives this constraint an intimate register: womanhood represented through maternity, care, loss, and symbolic burden, the body made legible by the roles it is asked to carry.[2] Mary Morrissy's account of Una Watters adds the everyday, where the woman is set inside ordinary weather, labor, and street life rather than idealized apart from it.[3]\n\nConstraint does not erase agency; it redirects it. The body still carries force, but that force is shaped by who is permitted to look and who is expected to be seen. The viewer is disciplined too. Each repeated crop, pose, and symbol teaches a visual habit, until seeing is no longer simple contact but compliance, resistance, and learned interpretation happening at once. The room has rules, and the eye has already agreed to most of them before it knows that it is choosing to obey.",
  "mediation": "The veil is an editing system, not a disappearance. Where the body and the rule meet a surface that can interrupt both, lace, shadow, fabric, blur, flowers, hair, and darkness become interfaces. They do not simply hide the figure; they decide how slowly it is allowed to arrive.\n\nA blocked face increases attention, because the viewer has to complete the missing information. Denial becomes structure. This is the logic the art of obstruction has always understood: Symbolism treats the visible world as a carrier for inward states, and Surrealism turns ordinary surfaces into dream pressure and psychological interruption.[4][5] The covered eye and the displaced face push the viewer toward interpretation rather than recognition.\n\nSo this section opens its grid and lets the images feel secretive, with more negative space and more surface. The body wants to appear; the rule wants to organize appearance; the veil controls the tempo of access. The point is not mystery for its own sake but cognitive pressure. A hidden gaze makes the eye work, and meaning arrives only through that effort. What is withheld is not absence; it is the part of the image still being decided.",
  "synthesis": "Sight becomes visceral when these forces remain active together. The final movement refuses to resolve the body, the rule, and the veil into a clean hierarchy. Agency begins the argument, constraint disciplines it, and mediation keeps it unresolved, and the image grows powerful precisely because no single force wins.\n\nThis is the thesis the whole issue has been building toward: psychological pressure does not come from clear depiction. It comes from calculated revelation, the image negotiating what can be seen, how quickly, and what stays withheld even after attention has been spent. The body is present but not fully available. Culture is legible but never neutral. The veil interrupts, yet it also teaches the eye how to continue.\n\nSo the closing pages keep the layout asymmetrical. Large images take authority; text presses beside them, slightly displaced. A symmetrical page would imply that sight had settled, and this argument needs sight to stay unstable, because instability is where looking turns into learning. The anatomy of looking is never finished. It only changes the surface it has to cross next, and asks the eye to begin the work again."
};

var SECTION = {
  "Agency": {
    "numeral": "I",
    "title": "Agency",
    "sub": "The Body / presence before permission",
    "blurb": "Agency is the body as its own first statement: a hand, an eye, a turned face that claims attention as pressure, before any rule arrives to explain it."
  },
  "Constraint": {
    "numeral": "II",
    "title": "Constraint",
    "sub": "The Rule / visibility as protocol",
    "blurb": "Constraint is culture turning visibility into protocol: pose, costume, rank, and ritual teach a body how it may appear, and teach the viewer how to approve it."
  },
  "Mediation": {
    "numeral": "III",
    "title": "Mediation",
    "sub": "The Veil / the tempo of access",
    "blurb": "Mediation is the veil as an editing system: lace, shadow, fabric, and blur do not simply hide the body, they decide how slowly it is allowed to be seen."
  },
  "Synthesis": {
    "numeral": "IV",
    "title": "Synthesis",
    "sub": "Sight that refuses to settle",
    "blurb": "Synthesis is sight that refuses to settle: body, rule, and veil stay active at once, so looking stays unfinished and the image keeps its pressure."
  }
};

var COVER_PATH = "/home/user/theory-of-sigh/images/cover.jpg";

function mm(v) { return v + "mm"; }
var DESIGN_W_MM = 210;
var DESIGN_H_MM = 297;
var PAGE_W_MM = 279.4;
var PAGE_H_MM = 215.9;
function sx(v) { return v * PAGE_W_MM / DESIGN_W_MM; }
function sy(v) { return v * PAGE_H_MM / DESIGN_H_MM; }
function b(t, l, bot, r) { return [mm(sy(t)), mm(sx(l)), mm(sy(bot)), mm(sx(r))]; }
function pageBounds(page, bounds) {
  var pb = page.bounds;
  var topOffset = Number(pb[0]);
  var leftOffset = Number(pb[1]);
  return [
    mm(topOffset + parseFloat(bounds[0])),
    mm(leftOffset + parseFloat(bounds[1])),
    mm(topOffset + parseFloat(bounds[2])),
    mm(leftOffset + parseFloat(bounds[3]))
  ];
}
function asset(i) { return ASSETS[i % ASSETS.length]; }
function assetByName(sub) {
  for (var i = 0; i < ASSETS.length; i++) {
    if (ASSETS[i].title.toLowerCase().indexOf(sub) >= 0) return ASSETS[i];
  }
  return null;
}

function groupAsset(groupName, i) {
  var matches = [];
  for (var a = 0; a < ASSETS.length; a++) {
    if (ASSETS[a].group.indexOf(groupName) >= 0) matches.push(ASSETS[a]);
  }
  if (matches.length === 0) return asset(i);
  return matches[i % matches.length];
}

function copyChunk(key, n) {
  var text = COPY[key] || COPY.synthesis;
  var words = text.replace(/\r|\n/g, " ").split(/\s+/);
  var wordsPerPage = 86;
  var chunks = [];
  var i = 0;
  while (i < words.length) {
    var end = Math.min(i + wordsPerPage, words.length);
    while (end < words.length) {
      var last = words[end - 1].charAt(words[end - 1].length - 1);
      if (last === "." || last === "!" || last === "?") break;
      end++;
    }
    chunks.push(words.slice(i, end).join(" "));
    i = end;
  }
  var startPage = key === "agency" ? 9 : key === "constraint" ? 18 : key === "mediation" ? 28 : 40;
  var offset = Math.max(0, n - startPage);
  return (offset < chunks.length) ? chunks[offset] : "";
}

function setupDoc() {
  var doc = app.documents.add();
  doc.documentPreferences.pageWidth = "279.4mm";
  doc.documentPreferences.pageHeight = "215.9mm";
  doc.documentPreferences.facingPages = true;
  doc.documentPreferences.pagesPerDocument = 50;
  doc.documentPreferences.documentBleedTopOffset = "3.175mm";
  doc.documentPreferences.documentBleedBottomOffset = "3.175mm";
  doc.documentPreferences.documentBleedInsideOrLeftOffset = "3.175mm";
  doc.documentPreferences.documentBleedOutsideOrRightOffset = "3.175mm";
  doc.marginPreferences.top = "16mm";
  doc.marginPreferences.bottom = "16mm";
  doc.marginPreferences.left = "16mm";
  doc.marginPreferences.right = "16mm";
  doc.marginPreferences.columnCount = 12;
  doc.marginPreferences.columnGutter = "5mm";
  return doc;
}

function builtinSwatch(doc, names) {
  for (var i = 0; i < names.length; i++) {
    try {
      var s = doc.swatches.itemByName(names[i]);
      if (s && s.isValid) return s;
    } catch (e) {}
    try {
      var s2 = doc.swatches.item(names[i]);
      if (s2 && s2.isValid) return s2;
    } catch (e2) {}
  }
  return doc.swatches.item(0);
}
function addSwatch(doc, name, values) {
  if (name === "Archival Cream") return builtinSwatch(doc, ["Paper", "[Paper]"]);
  return builtinSwatch(doc, ["Black", "[Black]"]);
}

function fitText(tf, minSize) {
  var attempts = 0;
  while (tf.overflows && attempts < 40) {
    try {
      var txt = tf.texts[0];
      txt.pointSize = Math.max(minSize, txt.pointSize - 0.35);
      txt.leading = txt.pointSize * 1.22;
    } catch (e) {}
    attempts++;
  }
}

function textFrame(page, bounds, text, size, fontStyle, swatch, opacity) {
  var tf = page.textFrames.add();
  tf.geometricBounds = pageBounds(page, bounds);
  tf.contents = text;
  try {
    tf.textFramePreferences.insetSpacing = ["2mm", "2mm", "2mm", "2mm"];
    tf.textFramePreferences.verticalJustification = VerticalJustification.TOP_ALIGN;
    tf.textFramePreferences.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
    tf.textFramePreferences.autoSizingType = AutoSizingTypeEnum.OFF;
    tf.textFramePreferences.useMinimumHeightForAutoSizing = true;
    tf.textFramePreferences.minimumHeightForAutoSizing = 8;
    tf.texts[0].appliedFont = app.fonts.item("Helvetica");
    tf.texts[0].fontStyle = fontStyle || "Regular";
    tf.texts[0].pointSize = size;
    tf.texts[0].leading = size * 1.22;
    tf.texts[0].fillColor = swatch;
  } catch (e) {}
  if (opacity < 100) {
    try { tf.transparencySettings.blendingSettings.opacity = opacity; } catch (e2) {}
  }
  fitText(tf, 5.5);
  return tf;
}

function imageFrame(page, bounds, item, opacity) {
  var rect = page.rectangles.add();
  rect.geometricBounds = pageBounds(page, bounds);
  rect.strokeWeight = 0;
  try {
    rect.place(File(item.path));
    rect.fit(FitOptions.FILL_PROPORTIONALLY);
    rect.fit(FitOptions.CENTER_CONTENT);
  } catch (e) {
    rect.fillColor = page.parent.parent.swatches.itemByName("[Black]");
  }
  if (opacity < 100) {
    try { rect.transparencySettings.blendingSettings.opacity = opacity; } catch (e2) {}
  }
  return rect;
}

function countMissingLinks(doc) {
  var missing = 0;
  for (var i = 0; i < doc.links.length; i++) {
    try {
      if (doc.links[i].status === LinkStatus.LINK_MISSING) missing++;
    } catch (e) {}
  }
  return missing;
}

function countOversetFrames(doc) {
  var overset = 0;
  for (var i = 0; i < doc.textFrames.length; i++) {
    try {
      if (doc.textFrames[i].isValid && doc.textFrames[i].overflows) overset++;
    } catch (e) {}
  }
  return overset;
}

function exportPdf(doc) {
  var pdfFile = File(OUTPUT_PDF);
  if (!pdfFile.parent.exists) pdfFile.parent.create();
  var preset = null;
  try {
    preset = app.pdfExportPresets.itemByName("[High Quality Print]");
    preset.name;
  } catch (e) {
    preset = app.pdfExportPresets.item(0);
  }
  doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, preset);
}

function writeBuildReport(doc) {
  var reportFile = File(OUTPUT_REPORT);
  if (!reportFile.parent.exists) reportFile.parent.create();
  var report = {
    document: "The Visceral Theory of Sight",
    generatedAt: new Date().toString(),
    pageCount: doc.pages.length,
    facingPages: doc.documentPreferences.facingPages,
    trim: "US Letter landscape 279.4mm x 215.9mm",
    bleed: "3.175mm all sides",
    columns: 12,
    assetCount: ASSETS.length,
    linkCount: doc.links.length,
    missingLinks: countMissingLinks(doc),
    textFrameCount: doc.textFrames.length,
    oversetTextFrames: countOversetFrames(doc),
    moodyLayoutRules: [
      "black and paper preflight base",
      "black-only accent tints for Digital Publishing profile",
      "large image fields",
      "overlap captions",
      "broken text flow",
      "full-bleed pressure pages",
      "layered translucent panels"
    ],
    outputs: {
      indd: OUTPUT_INDD,
      idml: OUTPUT_IDML,
      pdf: OUTPUT_PDF
    }
  };
  reportFile.encoding = "UTF-8";
  reportFile.open("w");
  reportFile.write(JSON.stringify(report, null, 2));
  reportFile.close();
}

function colorPanel(page, bounds, swatch, opacity) {
  var rect = page.rectangles.add();
  rect.geometricBounds = pageBounds(page, bounds);
  rect.strokeWeight = 0;
  rect.fillColor = swatch;
  try { rect.transparencySettings.blendingSettings.opacity = opacity; } catch (e) {}
  return rect;
}

function caption(page, bounds, item, ink, cream) {
  var theme = item.group.replace("Group 1: ", "").replace("Group 2: ", "").replace("Group 3: ", "");
  var label = item.id + " / " + theme + "\n" + (item.short_caption || item.caption || "");
  var tf = textFrame(page, bounds, label, 6.4, "Bold", cream, 100);
  try { tf.fillColor = cream; tf.transparencySettings.blendingSettings.opacity = 92; } catch(e) {}
  return tf;
}

function pageNum(page, n, ink) {
  textFrame(page, b(204, 250, 212, 270), ("0" + n).slice(-2), 6.5, "Regular", cream, 100);
}

function configurePreflight(doc) {
  // Color landscape magazine profile: duplicate Digital Publishing but allow
  // CMY plates (color photos) and landscape orientation. Mirrors the
  // Brooke Automation configurePublicationPreflight command.
  var profileName = "Anatomy of Looking - Color Landscape";
  var profile = null;
  try { profile = app.preflightProfiles.itemByName(profileName); profile.name; }
  catch (e) {
    try { profile = app.preflightProfiles.itemByName("kDigPubProfileName").duplicate(); profile.name = profileName; }
    catch (e2) { try { profile = app.preflightProfiles.add(); profile.name = profileName; } catch (e3) { return; } }
  }
  try { profile.description = "Color landscape magazine profile; CMY plates and landscape orientation intentionally allowed."; } catch (e4) {}
  try { profile.preflightProfileRules.itemByName("ADBE_CMYPlates").flag = 1699890274; } catch (e5) {}
  try { profile.preflightProfileRules.itemByName("ADBE_PageSizeOrientation").flag = 1699890274; } catch (e6) {}
  try {
    doc.preflightOptions.preflightWorkingProfile = profile;
    doc.preflightOptions.preflightOff = false;
  } catch (e7) {}
}

function saveDesktopFiles(doc) {
  var inddFile = File(OUTPUT_INDD);
  var idmlFile = File(OUTPUT_IDML);
  if (!inddFile.parent.exists) inddFile.parent.create();
  if (inddFile.exists) inddFile.remove();
  if (idmlFile.exists) idmlFile.remove();
  doc.save(inddFile);
  doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile);
  exportPdf(doc);
  writeBuildReport(doc);
}

function cover(page, doc, ink, cream, gold) {
  var item = groupAsset("Mediation", 0);
  if (COVER_PATH && File(COVER_PATH).exists) item = { path: COVER_PATH, id: "COVER", title: "Cover", group: "Mediation", caption: "", short_caption: "" };
  imageFrame(page, b(-4, -4, 220, 284), item, 100);
  colorPanel(page, b(120, -4, 220, 284), ink, 46);
  textFrame(page, b(150, 18, 162, 230), "THE ANATOMY OF LOOKING", 10, "Bold", gold, 100);
  textFrame(page, b(164, 18, 198, 252), "THE VISCERAL\rTHEORY OF SIGHT", 33, "Bold", cream, 100);
  textFrame(page, b(198, 18, 210, 232), "the body, the gaze, and the veil", 11, "Regular", cream, 100);
}

function sectionTitle(page, key, ink, cream, gold) {
  var meta = SECTION[key];
  var openerItem = (key === "Mediation") ? (assetByName("allef-vinicius") || groupAsset(key, 1)) : groupAsset(key, 1);
  imageFrame(page, b(-4, -4, 220, 284), openerItem, 100);
  colorPanel(page, b(-4, -4, 220, 284), ink, 56);
  textFrame(page, b(94, 18, 106, 180), "ARTICLE " + meta.numeral, 11, "Bold", gold, 100);
  textFrame(page, b(108, 18, 150, 252), meta.title, 38, "Bold", cream, 100);
  textFrame(page, b(150, 18, 164, 250), meta.sub, 12, "Italic", cream, 100);
  textFrame(page, b(166, 18, 202, 230), meta.blurb, 10, "Regular", cream, 100);
}

function frontMatter(page, n, doc, ink, cream, gold) {
  if (n === 2) {
    imageFrame(page, b(-4, -4, 220, 284), groupAsset("Mediation", 1), 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 40);
    textFrame(page, b(190, 18, 202, 220), "THE ANATOMY OF LOOKING", 10, "Bold", gold, 100);
  } else if (n === 3) {
    textFrame(page, b(18, 18, 30, 120), "TITLE", 11, "Bold", gold, 100);
    textFrame(page, b(34, 18, 96, 250), "THE VISCERAL\rTHEORY OF SIGHT", 40, "Bold", cream, 100);
    textFrame(page, b(98, 18, 118, 250), "A visual psychology issue on gaze, image memory, and the veil.", 13, "Regular", cream, 100);
    textFrame(page, b(150, 18, 200, 250), "This issue uses local image files supplied for production. Adobe Stock and Unsplash assets require license and source verification before public release. Citations are real and listed in Works Consulted; exact editions, page ranges, and licenses are confirmed before final print.", 9, "Regular", cream, 100);
  } else {
    textFrame(page, b(18, 18, 30, 220), "CONTENTS", 11, "Bold", gold, 100);
    textFrame(page, b(34, 18, 82, 250), "Agency / Constraint / Mediation", 34, "Bold", cream, 100);
    var tocTitles = "Front Matter\rIntroduction: The Visceral Theory of Sight\rI. Agency\rII. Constraint\rIII. Mediation\rIV. Synthesis\rBack Matter";
    textFrame(page, b(96, 18, 200, 215), tocTitles, 13, "Regular", cream, 100);
    var pf = textFrame(page, b(96, 215, 200, 255), "01\r05\r08\r17\r27\r39\r46", 13, "Bold", gold, 100);
    try { pf.texts[0].justification = Justification.RIGHT_ALIGN; } catch (e) {}
  }
}

function introPage(page, n, doc, ink, cream, gold) {
  if (n === 5) {
    textFrame(page, b(20, 18, 52, 200), "The Visceral Theory of Sight", 26, "Bold", cream, 100);
    textFrame(page, b(58, 18, 180, 150), COPY.intro, 10.5, "Regular", cream, 100);
    imageFrame(page, b(20, 158, 118, 252), groupAsset("Mediation", n), 100);
    imageFrame(page, b(122, 158, 199, 252), groupAsset("Agency", n), 100);
    caption(page, b(102, 162, 118, 248), groupAsset("Mediation", n), ink, cream);
  } else if (n === 6) {
    imageFrame(page, b(-4, -4, 220, 284), groupAsset("Constraint", n), 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 48);
    textFrame(page, b(148, 18, 186, 250), "The image does not give itself all at once.", 26, "Bold", cream, 100);
    textFrame(page, b(186, 18, 200, 252), "Controlled revelation is the method. Tension is the evidence.", 11, "Regular", cream, 100);
  } else {
    textFrame(page, b(18, 18, 30, 220), "THE THREE PRESSURES", 12, "Bold", gold, 100);
    textFrame(page, b(40, 18, 70, 96), "AGENCY\rbody as force", 14, "Bold", cream, 100);
    textFrame(page, b(40, 100, 70, 178), "CONSTRAINT\rbody as protocol", 14, "Bold", cream, 100);
    textFrame(page, b(40, 182, 70, 262), "MEDIATION\rveil as edit", 14, "Bold", cream, 100);
    imageFrame(page, b(80, 18, 150, 263), groupAsset("Agency", n), 100);
    textFrame(page, b(156, 18, 198, 255), COPY.intro, 9.5, "Regular", cream, 100);
  }
}

function articlePage(page, n, section, item, item2, item3, doc, ink, cream, gold, slate) {
  var mode = n % 3;
  var body = copyChunk(section.toLowerCase(), n);
  if (!body) {
    imageFrame(page, b(-4, -4, 220, 284), item, 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 30);
    textFrame(page, b(18, 18, 30, 220), section + " / SEQUENCE", 9, "Bold", gold, 100);
    caption(page, b(176, 18, 200, 150), item, ink, cream);
    return;
  }
  if (mode === 0) {
    // Dominant image left, text column right.
    imageFrame(page, b(16, 16, 199, 150), item, 100);
    textFrame(page, b(20, 160, 44, 262), section, 20, "Bold", cream, 100);
    textFrame(page, b(46, 160, 199, 262), body, 9.2, "Regular", cream, 100);
    caption(page, b(180, 20, 199, 110), item, ink, cream);
  } else if (mode === 1) {
    // Full-bleed image, scrim, pull statement, body panel.
    imageFrame(page, b(-4, -4, 220, 284), item, 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 50);
    textFrame(page, b(20, 18, 26, 170), "ARTICLE / " + section, 8, "Bold", gold, 100);
    textFrame(page, b(30, 18, 74, 240), "Only one eye remains; the image gets louder.", 24, "Bold", cream, 100);
    colorPanel(page, b(150, 12, 200, 150), ink, 58);
    textFrame(page, b(154, 18, 198, 146), body, 8.6, "Regular", cream, 100);
  } else {
    // Triptych: three images across, text band beneath (multi-image spread).
    imageFrame(page, b(16, 16, 132, 95), item, 100);
    imageFrame(page, b(16, 100, 132, 179), item2, 100);
    imageFrame(page, b(16, 184, 132, 263), item3, 100);
    textFrame(page, b(140, 16, 162, 262), section + " / SEQUENCE", 16, "Bold", cream, 100);
    textFrame(page, b(164, 16, 199, 262), body, 9, "Regular", cream, 100);
    caption(page, b(116, 104, 132, 175), item2, ink, cream);
  }
}

function backMatter(page, n, doc, ink, cream, gold) {
  if (n === 50) {
    textFrame(page, b(40, 18, 96, 230), "Sight remains unfinished.", 34, "Bold", cream, 100);
    textFrame(page, b(150, 18, 190, 250), "Every act of looking leaves a remainder: memory, attention, and the need to interpret what the eye cannot settle.", 10, "Regular", cream, 100);
    return;
  }
  var head = n === 46 ? "IMAGE SOURCE REGISTER" : n === 47 ? "IMAGE SOURCE REGISTER / CONTINUED" : n === 48 ? "SOURCE LIST" : "COLOPHON";
  textFrame(page, b(18, 18, 34, 255), head, 14, "Bold", gold, 100);
  if (n === 46 || n === 47) {
    var startIdx = n === 46 ? 0 : 32;
    var lines = "";
    for (var i = startIdx; i < Math.min(startIdx + 32, ASSETS.length); i++) {
      lines += ASSETS[i].id + "  " + ASSETS[i].title + " - rights verify\r";
    }
    textFrame(page, b(40, 18, 200, 255), lines, 8, "Regular", cream, 100);
  } else if (n === 48) {
    textFrame(page, b(40, 18, 200, 255), "McDermott: Paleolithic agency and the body. Havelock/Reeder: Greek art, cultural constraint, posture, social rule. Veiling iconography / Vera Icona / lace / mediation theory. Verify all exact source details before final export. No direct quotations are used because source texts were not supplied.", 10, "Regular", cream, 100);
  } else {
    textFrame(page, b(40, 18, 200, 255), "The Visceral Theory of Sight is a visual-psychology issue on gaze, image memory, and the veil. Photographs are credited in the Image Source Register; scholarly works are listed under Works Consulted. Set in Gloock, Spectral, and Work Sans; printed white on black.", 10, "Regular", cream, 100);
  }
}

function releaseOpenOutputDoc() {
  var outputFile = File(OUTPUT_INDD);
  for (var d = app.documents.length - 1; d >= 0; d--) {
    try {
      var openDoc = app.documents[d];
      if (openDoc.fullName && openDoc.fullName.fsName === outputFile.fsName) {
        var stamp = new Date().getTime();
        var backup = File(outputFile.parent.fsName + "/the-visceral-theory-of-sight-50pp-preflight-backup-" + stamp + ".indd");
        openDoc.save(backup);
        openDoc.close(SaveOptions.NO);
      }
    } catch (e) {}
  }
}

releaseOpenOutputDoc();
var doc = setupDoc();
var ink = addSwatch(doc, "Ink", [17, 16, 14]);
var cream = addSwatch(doc, "Archival Cream", [243, 235, 221]);
var gold = addSwatch(doc, "Muted Gold", [165, 130, 66]);
var slate = addSwatch(doc, "Slate Blue", [82, 107, 122]);

for (var p = 0; p < doc.pages.length; p++) {
  var page = doc.pages[p];
  var n = p + 1;
  colorPanel(page, b(-4, -4, 220, 284), ink, 100);
  if (n === 1) cover(page, doc, ink, cream, gold);
  else if (n <= 4) frontMatter(page, n, doc, ink, cream, gold);
  else if (n <= 7) introPage(page, n, doc, ink, cream, gold);
  else if (n === 8) sectionTitle(page, "Agency", ink, cream, gold);
  else if (n <= 16) articlePage(page, n, "AGENCY", groupAsset("Agency", n), groupAsset("Agency", n + 1), groupAsset("Agency", n + 2), doc, ink, cream, gold, slate);
  else if (n === 17) sectionTitle(page, "Constraint", ink, cream, gold);
  else if (n <= 26) articlePage(page, n, "CONSTRAINT", groupAsset("Constraint", n), groupAsset("Constraint", n + 1), groupAsset("Constraint", n + 2), doc, ink, cream, gold, slate);
  else if (n === 27) sectionTitle(page, "Mediation", ink, cream, gold);
  else if (n <= 38) articlePage(page, n, "MEDIATION", groupAsset("Mediation", n), groupAsset("Mediation", n + 1), groupAsset("Mediation", n + 2), doc, ink, cream, gold, slate);
  else if (n === 39) sectionTitle(page, "Synthesis", ink, cream, gold);
  else if (n <= 45) articlePage(page, n, "SYNTHESIS", asset(n), asset(n + 1), asset(n + 2), doc, ink, cream, gold, slate);
  else backMatter(page, n, doc, ink, cream, gold);
  pageNum(page, n, ink);
}

// Final overset guard.
for (var i = 0; i < doc.textFrames.length; i++) {
  if (doc.textFrames[i].overflows) fitText(doc.textFrames[i], 5.5);
}

configurePreflight(doc);
saveDesktopFiles(doc);
} catch (err) {
  var errorFile = File("/home/user/theory-of-sigh/visceral-production-route/reports/indesign-preflight-safe-error.txt");
  if (!errorFile.parent.exists) errorFile.parent.create();
  errorFile.encoding = "UTF-8";
  errorFile.open("w");
  errorFile.write("line: " + err.line + "\nmessage: " + err.message + "\nname: " + err.name);
  errorFile.close();
  throw err;
}
