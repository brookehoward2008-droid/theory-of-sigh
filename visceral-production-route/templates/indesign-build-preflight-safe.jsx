// The Visceral Theory of Sight - full 50-page InDesign layout builder
// Run from InDesign: File > Scripts > Other Script...
// Builds US Letter landscape facing pages, 0.125in bleed, 12-column grid, K-only linked images, captions, layered editorial modules, PDF, and audit report.

var ASSETS = [
  {
    "id": "A01",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-01-konly.jpg",
    "title": "a01-mediation-a-photograph-of-an-attractive-woman-with-a-w",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A02",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-02-konly.jpg",
    "title": "a05-social-constraint-adobestock-1024472839",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A03",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-03-konly.jpg",
    "title": "a06-social-constraint-adobestock-1040196803",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A04",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-04-konly.jpg",
    "title": "a07-social-constraint-adobestock-1044937382",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A05",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-05-konly.jpg",
    "title": "a08-social-constraint-adobestock-1225023891",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A06",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-06-konly.jpg",
    "title": "a09-social-constraint-adobestock-140076283",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A07",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-07-konly.jpg",
    "title": "a10-social-constraint-adobestock-1462135790",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A08",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-08-konly.jpg",
    "title": "a11-social-constraint-adobestock-206067082",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A09",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-09-konly.jpg",
    "title": "a12-social-constraint-adobestock-268225510",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A10",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-10-konly.jpg",
    "title": "a13-social-constraint-adobestock-320500758",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A11",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-11-konly.jpg",
    "title": "a14-social-constraint-adobestock-368079012",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A12",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-12-konly.jpg",
    "title": "a15-social-constraint-adobestock-378198491",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A13",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-13-konly.jpg",
    "title": "a16-social-constraint-adobestock-565582008",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A14",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-14-konly.jpg",
    "title": "a17-social-constraint-adobestock-720156971",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A15",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-15-konly.jpg",
    "title": "a18-social-constraint-adobestock-730927617",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A16",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-16-konly.jpg",
    "title": "a19-social-constraint-adobestock-973721353",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A17",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-17-konly.jpg",
    "title": "a20-mediation-alex-bracken-l1sjo7tmvec-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A18",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-18-konly.jpg",
    "title": "a21-raw-agency-alexander-krivitskiy-az7rqwlwkhi-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A19",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-19-konly.jpg",
    "title": "a22-social-constraint-alexander-krivitskiy-gfopukdkmvo-uns",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A20",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-20-konly.jpg",
    "title": "a23-mediation-allef-vinicius-dkrntf-jgtw-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A21",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-21-konly.jpg",
    "title": "a24-raw-agency-amir-geshani-2jh8d3chnec-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A22",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-22-konly.jpg",
    "title": "a25-social-constraint-andrey-zvyagintsev-t8iknlqojcq-unspl",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A23",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-23-konly.jpg",
    "title": "a26-mediation-arielle-allouche-h82rqe4gria-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A24",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-24-konly.jpg",
    "title": "a27-raw-agency-baran-lotfollahi-lobgof8rurg-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A25",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-25-konly.jpg",
    "title": "a28-social-constraint-birmingham-museums-trust-oqpbewogd0o",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A26",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-26-konly.jpg",
    "title": "a29-mediation-boston-public-library-grbfmxpumu4-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A27",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-27-konly.jpg",
    "title": "a30-raw-agency-brunxs-monochrome-spniqdcpi9u-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A28",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-28-konly.jpg",
    "title": "a31-social-constraint-caleb-kastein-lmnz6-icim8-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A29",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-29-konly.jpg",
    "title": "a32-mediation-camila-quintero-franco-mc852jack1g-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A30",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-30-konly.jpg",
    "title": "a33-raw-agency-carl-cheng-o4l-vetcxhy-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A31",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-31-konly.jpg",
    "title": "a34-social-constraint-cole-keister-d6zqt8nfiq4-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A32",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-32-konly.jpg",
    "title": "a35-mediation-darius-bashar-3xegkkbinck-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A33",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-33-konly.jpg",
    "title": "a36-raw-agency-drew-dizzy-graham-ctkgzjtmjqu-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A34",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-34-konly.jpg",
    "title": "a37-social-constraint-elias-maurer-ssplu7ipc8g-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A35",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-35-konly.jpg",
    "title": "a38-mediation-elvis-kaiser-rqbk5ez6qa0-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A36",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-36-konly.jpg",
    "title": "a39-raw-agency-enesh-taganova-ioxgidqvqyq-unsplash-1",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A37",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-37-konly.jpg",
    "title": "a40-social-constraint-erik-mclean-gjtz5ckgeew-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A38",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-38-konly.jpg",
    "title": "a41-mediation-europeana-lbt8newonko-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A39",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-39-konly.jpg",
    "title": "a42-raw-agency-europeana-wwghncxmcqi-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A40",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-40-konly.jpg",
    "title": "a43-social-constraint-evilicio-inc-1hty8zlswls-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A41",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-41-konly.jpg",
    "title": "a44-mediation-flaviu-costin-vr-sbbcwklc-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A42",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-42-konly.jpg",
    "title": "a45-raw-agency-good-faces-r8vsytyy2oe-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A43",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-43-konly.jpg",
    "title": "a46-social-constraint-harry-quan-g1iycecw2ei-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A44",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-44-konly.jpg",
    "title": "a47-mediation-igor-rand-giw9ccl3hxa-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A45",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-45-konly.jpg",
    "title": "a48-raw-agency-ilya-mondryk-oceeo0ayn1s-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A46",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-46-konly.jpg",
    "title": "a49-social-constraint-janko-ferlic-brzt6bdt6na-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A47",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-47-konly.jpg",
    "title": "a50-mediation-jr-korpa-0lokelbdsbw-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A48",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-48-konly.jpg",
    "title": "a51-raw-agency-library-of-congress-v0jinhbf3xq-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A49",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-49-konly.jpg",
    "title": "a52-social-constraint-lorraine-hill-4dyxkga2gxa-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A50",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-50-konly.jpg",
    "title": "a53-mediation-mahdi-bafande-rw-azxeky7q-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A51",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-51-konly.jpg",
    "title": "a54-raw-agency-nastia-petruk-f-hajyv3wye-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A52",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-52-konly.jpg",
    "title": "a55-social-constraint-nina-zeynep-guler-fjjivsx-bxm-unspla",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A53",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-53-konly.jpg",
    "title": "a56-mediation-noah-buscher-11ldehfy-ha-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A54",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-54-konly.jpg",
    "title": "a57-raw-agency-ovie-ogege-6bwt4ci-ujs-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A55",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-55-konly.jpg",
    "title": "a58-social-constraint-see-plus-np3s9byoqac-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A56",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-56-konly.jpg",
    "title": "a59-mediation-smithsonian-elpq3w9epnk-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A57",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-57-konly.jpg",
    "title": "a60-raw-agency-smithsonian-otg-zz0tybe-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A58",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-58-konly.jpg",
    "title": "a61-social-constraint-teslariu-mihai-tk-szddiuis-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A59",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-59-konly.jpg",
    "title": "a62-mediation-the-new-york-public-library-ndjv4ntdf6g-unsp",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A60",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-60-konly.jpg",
    "title": "a63-raw-agency-toa-heftiba-fv1lunshcaw-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A61",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-61-konly.jpg",
    "title": "a64-social-constraint-umanoide-xjp9ak1oqhw-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A62",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-62-konly.jpg",
    "title": "a65-mediation-umesh-soni-hpklbuuel-k-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A63",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-63-konly.jpg",
    "title": "a66-mediation-woman-obscured-by-white-flowers-creating-a-d",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A64",
    "path": "/home/user/theory-of-sigh/visceral-production-route/assets/preflight-konly/asset-64-konly.jpg",
    "title": "a67-social-constraint-zachary-kadolph-qbjgfnctwbu-unsplash",
    "group": "Group 2: Social Constraint"
  }
];
var OUTPUT_INDD = "/home/user/theory-of-sigh/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.indd";
var OUTPUT_IDML = "/home/user/theory-of-sigh/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.idml";
var OUTPUT_PDF = "/home/user/theory-of-sigh/visceral-production-route/output/pdf/the-visceral-theory-of-sight-50pp-indesign-auto.pdf";
var OUTPUT_REPORT = "/home/user/theory-of-sigh/visceral-production-route/reports/indesign-preflight-safe-build-report.json";

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

try {

var COPY = {
  "intro": "Sight is never only an act of seeing. It is a negotiation between the body that appears, the culture that disciplines appearance, and the surface that decides what can be touched by the eye. This book moves through agency, constraint, and mediation as one visual pressure system.",
  "agency": "The body becomes the first instrument of authorship before it becomes a subject for interpretation. In the first movement of this book, sight begins with bodily insistence: a hand, a shoulder, a mouth, an eye, or a turned face does not wait for culture to explain it. The figure enters as pressure. It occupies the page with the blunt force of being present, and that presence matters because the viewer has not yet been given a stable rule for reading it.\n\nThe scholarly route through McDermott is used here as a verified-to-be-checked framework rather than as a source of direct quotation. The working idea is that early bodily images can be read as more than passive objects of display. They carry agency through scale, fragment, gesture, and emphasis. A figure can be partial and still be active. A cropped body can still claim space. The page therefore treats the body as origin, not because origin is simple, but because every later system of looking must first meet the fact of the body.\n\nAgency in this layout is close, image-led, and slightly uncomfortable. The images press into the margins. Captions cross edges. Text is broken into short forceful passages so the reader feels the body interrupting analysis. The design does not let the article become smooth because smoothness would weaken the argument. The body is not introduced as an illustration of theory. It is introduced as the condition that makes theory necessary.\n\nThis is also where the neural learning backdrop enters quietly: looking is not passive reception. The eye learns by comparing pressure, repetition, interruption, and contrast. A body seen once is an image. A body seen across a sequence becomes a pattern the reader has to train against. The first article therefore builds a visual lesson in agency: presence arrives before permission.",
  "constraint": "Culture turns visibility into a protocol. The second movement begins when bodily force is no longer allowed to stand alone. The figure becomes arranged by posture, costume, rank, gender, ritual, and inherited rules of display. A face can still look outward, but it now looks through an architecture of expectation. A body can still occupy the frame, but the frame has begun to instruct it.\n\nThe Havelock and Reeder route is treated as a scholarly placeholder for the cultural body: Greek art, social posture, public presentation, and the disciplined relation between figure and viewer. No direct quotation is used here because the source texts are not supplied in the workspace. Instead, the article synthesizes the assigned idea: visibility becomes social when a culture teaches bodies how to appear, and teaches viewers how to approve that appearance.\n\nConstraint does not erase agency. It redirects it. The body still carries force, but that force is shaped by protocol. The page system responds by tightening. Columns become more formal. Panels sit closer to the grid. Accent color marks pressure points, especially where the terms agency and constraint appear together. This section should feel less wild than the first, but more tense. The reader should sense that the body has entered a room where every gesture is already being measured.\n\nThis matters to the theory of sight because the viewer is also constrained. We do not only look at the ruled body; we learn the rule by looking. The layout asks the reader to notice that training. Each repeated crop, caption, and column teaches a visual habit. The eye becomes disciplined alongside the figure. Seeing is no longer just contact. It is compliance, resistance, and learned interpretation happening at the same time.",
  "mediation": "The veil is an editing system, not a disappearance. The third movement begins where the body and the rule meet a surface that can interrupt both. Lace, shadow, fabric, blur, flowers, hair, hands, and darkness all become interfaces. They do not simply hide the figure. They decide how slowly the figure can arrive.\n\nThe veiling route is held through iconography, Vera Icona, lace, secrecy, and the larger problem of mediated access. The key point is not that the viewer is denied. The key point is that denial becomes structure. A veil produces a special kind of attention because the eye has to work without full possession. It keeps searching, comparing edges, reading textures, and inventing continuity from fragments.\n\nThis section opens the grid. The design becomes more atmospheric, with more negative space and more surface interruption. Images are allowed to feel secretive. Text becomes quieter, more breath-based, but it still carries an argument: mediation is the place where agency and constraint become visible as tension. The body wants to appear. The rule wants to organize appearance. The veil controls the tempo of access.\n\nFor an ADHD reader, this section should not become vague. The idea stays modular: surface, delay, pressure, partial access. Those repeated terms create a learning path through the atmosphere. The reader can feel the mystery without getting lost inside it. The veil does not remove meaning. It makes meaning arrive through effort.",
  "synthesis": "Sight becomes visceral when these forces remain active together. The final movement refuses to solve the body, the rule, and the veil into a clean hierarchy. Agency begins the argument, constraint disciplines it, and mediation keeps it unresolved. The image becomes powerful because no single force wins.\n\nThis is the core thesis of the book: psychological pressure does not come from clear depiction alone. It comes from calculated revelation. The viewer feels the image because the image negotiates what can be seen, how quickly it can be seen, and what remains withheld even after attention has been spent. The body is present, but not fully available. Culture is legible, but not neutral. The veil interrupts, but also teaches the eye how to continue.\n\nThe synthesis pages therefore break the grid most visibly. Large images take authority. Text floats beside them or presses into panels that seem slightly displaced. The asymmetry is not decoration. It is the final proof of the argument. A symmetrical page would imply that sight has settled. This book needs sight to remain unstable, because unstable sight is where learning happens.\n\nThe conclusion keeps the claims rights-sensitive and citation-safe. It does not invent quotations, publication details, or license certainty. It names the scholarly routes that still need final verification and holds the visual argument as the completed local production route. What remains is deliberate: source checking, instructor review, and final export. The theory, however, is already visible in the structure."
};

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
  var startPage = key === "agency" ? 8 : key === "constraint" ? 17 : key === "mediation" ? 27 : 39;
  var offset = Math.max(0, n - startPage);
  var wordsPerPage = 52;
  var start = Math.min(offset * wordsPerPage, Math.max(0, words.length - wordsPerPage));
  return words.slice(start, start + wordsPerPage).join(" ");
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
  doc.marginPreferences.top = "15.113mm";
  doc.marginPreferences.bottom = "15.113mm";
  doc.marginPreferences.left = "27.940mm";
  doc.marginPreferences.right = "20.955mm";
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
  while (tf.overflows && attempts < 18) {
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
    tf.textFramePreferences.autoSizingType = AutoSizingTypeEnum.HEIGHT_ONLY;
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
  fitText(tf, 6.5);
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
  var label = item.id + " / " + item.group.replace("Group 1: ", "").replace("Group 2: ", "").replace("Group 3: ", "") + "\ncaption crosses the image edge; rights verify";
  var tf = textFrame(page, bounds, label, 6.2, "Bold", cream, 100);
  try { tf.fillColor = ink; tf.transparencySettings.blendingSettings.opacity = 78; } catch(e) {}
  return tf;
}

function pageNum(page, n, ink) {
  textFrame(page, b(282, 184, 289, 202), ("0" + n).slice(-2), 6.5, "Regular", ink, 100);
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
  colorPanel(page, b(0, 0, 297, 210), ink, 100);
  imageFrame(page, b(30, 24, 232, 186), item, 100);
  textFrame(page, b(240, 28, 269, 182), "THE VISCERAL\rTHEORY OF SIGHT", 24, "Bold", cream, 100);
  textFrame(page, b(270, 62, 282, 148), "the body, the gaze, and the veil", 8, "Regular", cream, 100);
}

function frontMatter(page, n, doc, ink, cream, gold) {
  if (n === 2) {
    textFrame(page, b(62, 24, 118, 170), "The Visceral\rTheory of Sight", 30, "Bold", ink, 100);
    textFrame(page, b(126, 26, 152, 160), "A 50-page editorial art book on controlled revelation.", 10, "Regular", ink, 100);
    textFrame(page, b(245, 24, 272, 160), "US Letter landscape preflight layout. 12-column grid. 0.125in bleed. Source and rights verification required before final export.", 7, "Regular", ink, 100);
  } else if (n === 3) {
    textFrame(page, b(216, 24, 271, 182), "LEGAL / CREDITS\rThis layout uses supplied local image files. Adobe Stock, Unsplash, and unknown local assets must be verified before public export. No direct quotations are used because source texts were not supplied.", 8, "Regular", ink, 100);
  } else {
    textFrame(page, b(42, 24, 70, 170), "BODY / RULE / VEIL", 24, "Bold", ink, 100);
    textFrame(page, b(96, 24, 196, 70), "01 Front Matter\r05 Introduction\r08 The Body", 11, "Regular", ink, 100);
    textFrame(page, b(126, 88, 226, 134), "17 Constraint\r27 The Veil\r39 Synthesis", 11, "Regular", gold, 100);
    textFrame(page, b(156, 150, 244, 190), "46 Credits\r48 Sources\r49 Process\r50 Close", 11, "Regular", ink, 100);
  }
}

function introPage(page, n, doc, ink, cream, gold) {
  imageFrame(page, b(32, 24, 132, 84), groupAsset("Mediation", n), 100);
  imageFrame(page, b(88, 98, 178, 186), groupAsset("Constraint", n), 100);
  imageFrame(page, b(154, 44, 238, 132), groupAsset("Agency", n), 85);
  colorPanel(page, b(188, 18, 252, 156), cream, 88);
  textFrame(page, b(196, 26, 224, 148), "The Visceral Theory of Sight", 21, "Bold", ink, 100);
  textFrame(page, b(226, 27, 258, 160), COPY.intro, 8.6, "Regular", ink, 100);
  caption(page, b(124, 72, 145, 134), groupAsset("Mediation", n), ink, cream);
}

function articlePage(page, n, section, item, doc, ink, cream, gold, slate) {
  var mode = n % 6;
  var accent = section === "MEDIATION" ? slate : gold;
  if (mode === 0) {
    imageFrame(page, b(24, 14, 216, 142), item, 100);
    colorPanel(page, b(144, 122, 205, 194), cream, 86);
    textFrame(page, b(152, 130, 176, 188), section, 18, "Bold", ink, 100);
    textFrame(page, b(176, 130, 204, 188), copyChunk(section.toLowerCase(), n), 7.8, "Regular", ink, 100);
    caption(page, b(196, 24, 216, 92), item, ink, cream);
  } else if (mode === 1) {
    imageFrame(page, b(42, 68, 210, 196), item, 100);
    colorPanel(page, b(18, 22, 240, 58), accent, 100);
    textFrame(page, b(44, 28, 198, 52), section, 18, "Bold", cream, 100);
    colorPanel(page, b(206, 46, 248, 176), cream, 84);
    textFrame(page, b(212, 52, 246, 168), copyChunk(section.toLowerCase(), n), 7.4, "Regular", ink, 100);
  } else if (mode === 2) {
    imageFrame(page, b(0, 0, 297, 210), item, 100);
    colorPanel(page, b(78, 0, 116, 210), accent, 82);
    textFrame(page, b(82, 26, 112, 182), "ONLY ONE EYE REMAINS, THE IMAGE GETS LOUDER.", 18, "Bold", cream, 100);
    colorPanel(page, b(214, 18, 276, 86), ink, 72);
    textFrame(page, b(220, 24, 270, 80), copyChunk(section.toLowerCase(), n), 7.2, "Regular", cream, 100);
  } else if (mode === 3) {
    imageFrame(page, b(34, 20, 120, 102), item, 100);
    imageFrame(page, b(112, 92, 250, 182), item, 92);
    textFrame(page, b(124, 28, 164, 128), "A body becomes legible through pressure.", 13, "Bold", ink, 100);
    textFrame(page, b(166, 28, 210, 118), copyChunk(section.toLowerCase(), n), 7.6, "Regular", ink, 100);
    caption(page, b(106, 78, 127, 148), item, ink, cream);
  } else if (mode === 4) {
    imageFrame(page, b(42, 30, 226, 180), item, 100);
    colorPanel(page, b(214, 0, 260, 210), accent, 88);
    textFrame(page, b(220, 22, 254, 188), "THE VEIL DOES NOT DISAPPEAR THE BODY.", 16, "Bold", cream, 100);
    colorPanel(page, b(68, 132, 116, 194), cream, 82);
    textFrame(page, b(72, 138, 112, 188), copyChunk(section.toLowerCase(), n), 7.2, "Regular", ink, 100);
  } else {
    imageFrame(page, b(22, 44, 266, 178), item, 100);
    colorPanel(page, b(26, 28, 58, 128), cream, 80);
    textFrame(page, b(30, 34, 54, 122), section + " / controlled visibility", 12, "Bold", ink, 100);
    caption(page, b(240, 120, 264, 190), item, ink, cream);
  }
}

function backMatter(page, n, doc, ink, cream, gold) {
  if (n === 50) {
    textFrame(page, b(60, 24, 108, 172), "Sight remains\runfinished.", 28, "Bold", ink, 100);
    textFrame(page, b(236, 24, 260, 172), "Final export still requires source verification, license verification, and instructor-facing review.", 8, "Regular", ink, 100);
  } else {
    var head = n === 46 ? "IMAGE CREDITS" : n === 47 ? "IMAGE CREDITS CONTINUED" : n === 48 ? "SOURCE LIST" : "PROCESS NOTES";
    textFrame(page, b(28, 24, 48, 172), head, 16, "Bold", ink, 100);
    var body = "Assets are linked from the production asset folder. Rights remain verify before final export. The layout uses overlap, broken flow, and layered pull-quote pressure to support agency, constraint, and mediation.";
    textFrame(page, b(64, 24, 246, 172), body, 8.5, "Regular", ink, 100);
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
  colorPanel(page, b(0, 0, 297, 210), cream, 100);
  if (n === 1) cover(page, doc, ink, cream, gold);
  else if (n <= 4) frontMatter(page, n, doc, ink, cream, gold);
  else if (n <= 7) introPage(page, n, doc, ink, cream, gold);
  else if (n <= 16) articlePage(page, n, "AGENCY", groupAsset("Agency", n), doc, ink, cream, gold, slate);
  else if (n <= 26) articlePage(page, n, "CONSTRAINT", groupAsset("Constraint", n), doc, ink, cream, gold, slate);
  else if (n <= 38) articlePage(page, n, "MEDIATION", groupAsset("Mediation", n), doc, ink, cream, gold, slate);
  else if (n <= 45) articlePage(page, n, "SYNTHESIS", asset(n), doc, ink, cream, gold, slate);
  else backMatter(page, n, doc, ink, cream, gold);
  pageNum(page, n, ink);
}

// Final overset guard.
for (var i = 0; i < doc.textFrames.length; i++) {
  if (doc.textFrames[i].overflows) fitText(doc.textFrames[i], 6.5);
}

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
