// The Anatomy of Looking - full 50-page InDesign issue builder
// Run from InDesign: File > Scripts > Other Script...
// Builds the print issue, linked image sequence, PDF proof, and audit report.

var ASSETS = [
  {
    "id": "A01",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-01.jpeg",
    "title": "A photograph of an attractive woman with a white lace blin",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A05",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-05.jpeg",
    "title": "AdobeStock_1024472839",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A06",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-06.jpeg",
    "title": "AdobeStock_1040196803",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A07",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-07.jpeg",
    "title": "AdobeStock_1044937382",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A08",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-08.jpeg",
    "title": "AdobeStock_1225023891",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A09",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-09.jpeg",
    "title": "AdobeStock_140076283",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A10",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-10.jpeg",
    "title": "AdobeStock_1462135790",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A11",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-11.jpeg",
    "title": "AdobeStock_206067082",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A12",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-12.jpeg",
    "title": "AdobeStock_268225510",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A13",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-13.jpeg",
    "title": "AdobeStock_320500758",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A14",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-14.jpeg",
    "title": "AdobeStock_368079012",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A15",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-15.jpeg",
    "title": "AdobeStock_378198491",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A16",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-16.jpeg",
    "title": "AdobeStock_565582008",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A17",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-17.jpeg",
    "title": "AdobeStock_720156971",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A18",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-18.jpeg",
    "title": "AdobeStock_730927617",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A19",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-19.jpeg",
    "title": "AdobeStock_973721353",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A20",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-20.jpg",
    "title": "alex-bracken-l1SJO7TMVEc-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A21",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-21.jpg",
    "title": "alexander-krivitskiy-az7rqWLWkhI-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A22",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-22.jpg",
    "title": "alexander-krivitskiy-GfOpUKdkMvo-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A23",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-23.jpg",
    "title": "allef-vinicius-DKrNTF_Jgtw-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A24",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-24.jpg",
    "title": "amir-geshani-2JH8d3ChNec-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A25",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-25.jpg",
    "title": "andrey-zvyagintsev-T8IkNlQojCQ-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A26",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-26.jpg",
    "title": "arielle-allouche-H82Rqe4griA-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A27",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-27.jpg",
    "title": "baran-lotfollahi-LOBgOf8Rurg-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A28",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-28.jpg",
    "title": "birmingham-museums-trust-oQpbeWoGD0o-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A29",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-29.jpg",
    "title": "boston-public-library-gRbFMxpUMU4-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A30",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-30.jpg",
    "title": "brunxs-monochrome-sPnIqdCPI9U-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A31",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-31.jpg",
    "title": "caleb-kastein-lmNz6-ICIM8-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A32",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-32.jpg",
    "title": "camila-quintero-franco-mC852jACK1g-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A33",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-33.jpg",
    "title": "carl-cheng-o4L-veTcXHY-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A34",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-34.jpg",
    "title": "cole-keister-D6zQt8NfIq4-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A35",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-35.jpg",
    "title": "darius-bashar-3XEgKKBinCk-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A36",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-36.jpg",
    "title": "drew-dizzy-graham-cTKGZJTMJQU-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A37",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-37.jpg",
    "title": "elias-maurer-sSpLu7IPC8g-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A38",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-38.jpg",
    "title": "elvis-kaiser-Rqbk5ez6Qa0-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A39",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-39.jpg",
    "title": "enesh-taganova-IoXGIDqVqYQ-unsplash (1)",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A40",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-40.jpg",
    "title": "erik-mclean-gjtz5cKGEEw-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A41",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-41.jpg",
    "title": "europeana-lBt8NEWOnko-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A42",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-42.jpg",
    "title": "europeana-wwgHncxMcQI-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A43",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-43.jpg",
    "title": "evilicio-inc-1HTY8zLsWLs-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A44",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-44.jpg",
    "title": "flaviu-costin-Vr-sBbCWklc-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A45",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-45.jpg",
    "title": "good-faces-R8VSYtyY2oE-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A46",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-46.jpg",
    "title": "harry-quan-G1iYCeCW2EI-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A47",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-47.jpg",
    "title": "igor-rand-GIW9CCL3HxA-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A48",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-48.jpg",
    "title": "ilya-mondryk-OCEeo0aYN1s-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A49",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-49.jpg",
    "title": "janko-ferlic-brZT6bdt6NA-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A50",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-50.jpg",
    "title": "jr-korpa-0lOkeLbdsBw-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A51",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-51.jpg",
    "title": "library-of-congress-v0jInHBf3XQ-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A52",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-52.jpg",
    "title": "lorraine-hill-4dyXkga2GxA-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A53",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-53.jpg",
    "title": "mahdi-bafande-rw-AZxeky7Q-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A54",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-54.jpg",
    "title": "nastia-petruk-F-HAjYv3WyE-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A55",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-55.jpg",
    "title": "nina-zeynep-guler-fjJiVSX-BxM-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A56",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-56.jpg",
    "title": "noah-buscher-11lDEHFy_hA-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A57",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-57.jpg",
    "title": "ovie-ogege-6bwT4cI_UJs-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A58",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-58.jpg",
    "title": "see-plus-NP3s9BYOqAc-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A59",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-59.jpg",
    "title": "smithsonian-ELPq3W9Epnk-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A60",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-60.jpg",
    "title": "smithsonian-OtG-Zz0tYbE-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A61",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-61.jpg",
    "title": "teslariu-mihai-tK-SzdDiUIs-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A62",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-62.jpg",
    "title": "the-new-york-public-library-ndJV4ntdF6g-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A63",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-63.jpg",
    "title": "toa-heftiba-FV1LuNSHcAw-unsplash",
    "group": "Group 1: Raw Agency"
  },
  {
    "id": "A64",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-64.jpg",
    "title": "umanoide-XJP9Ak1oqHw-unsplash",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A65",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-65.jpg",
    "title": "umesh-soni-hpklBuuel_k-unsplash",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A66",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-66.jpeg",
    "title": "Woman obscured by white flowers, creating a dreamy and sur",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A67",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-67.jpg",
    "title": "zachary-kadolph-qBJgfnCTwbU-unsplash",
    "group": "Group 2: Social Constraint"
  }
];
var OUTPUT_INDD = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.indd";
var OUTPUT_IDML = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.idml";
var OUTPUT_PDF = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/output/pdf/the-visceral-theory-of-sight-50pp-indesign-auto.pdf";
var OUTPUT_REPORT = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/reports/indesign-full-layout-auto-report.json";

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

var COPY = {
  "intro": "Sight is never only an act of seeing. It is a negotiation between the body that appears, the culture that disciplines appearance, and the surface that decides what can be touched by the eye. This book moves through agency, constraint, and mediation as one visual pressure system.",
  "agency": "The body becomes the first instrument of authorship before it becomes a subject for interpretation. In the first movement of this issue, sight begins with bodily insistence: a hand, a shoulder, a mouth, an eye, or a turned face does not wait for culture to explain it. The figure enters as pressure. It occupies the field with the blunt force of being present, and that presence matters because the viewer has not yet been given a stable rule for reading it.\n\nMcDermott gives this article its earliest time marker: the female body can be read as more than a passive object of display. His argument around Upper Paleolithic figurines opens a different possibility: that bodily representation may also carry evidence of lived perception, self-reference, and embodied seeing. That matters because a body can be partial and still be active. A face can be interrupted and still hold attention. A hand can become the first sign of agency before the viewer has named the person. The issue treats the body as origin, not because origin is simple, but because every later system of looking must first meet the fact of the body.\n\nAgency is close, image-led, and slightly uncomfortable. Faces and fragments interrupt the viewer before the viewer has decided what kind of image this is. A direct stare can feel like contact. A hidden eye can feel like refusal. A turned face can feel like a body protecting its own interior life. The body is not an illustration of theory. It is the condition that makes theory necessary.\n\nThis is also where the neural-learning backdrop enters quietly. Looking is not passive reception. The eye learns by comparing pressure, repetition, interruption, and contrast. A body seen once is an image. A body seen across time becomes a pattern the reader has to interpret. The first article therefore builds a visual lesson in agency: presence arrives before permission.",
  "constraint": "Culture turns visibility into a protocol. The second movement begins when bodily force is no longer allowed to stand alone. The figure becomes arranged by posture, costume, rank, gender, ritual, and inherited rules of display. A face can still look outward, but it now looks through an architecture of expectation. A body can still occupy the frame, but the frame has begun to instruct it.\n\nThe movement through time matters here. Maternity, labor, beauty, mourning, ordinary weather, and public presence are not separate categories; they are visual roles that cultures attach to women. Mulley's study of Laura Muntz shows how maternity can be made symbolic, intimate, and burdened at once. Morrissy's work on Una Watters brings the woman back into everyday weather and street life, where representation is less idealized and more socially placed.\n\nConstraint does not erase agency. It redirects it. The body still carries force, but that force is shaped by context: who is permitted to look, who is expected to be seen, and what a culture teaches the viewer to accept as natural. This section feels less wild than the first, but more tense. The reader should sense that the body has entered a room where every gesture is already being measured.\n\nThis matters to the theory of sight because the viewer is also constrained. We do not only look at the ruled body; we learn the rule by looking. Repetition, obstruction, pose, and symbol teach the eye how social meaning attaches to bodies through time. The eye becomes disciplined alongside the figure. Seeing is no longer just contact. It is compliance, resistance, and learned interpretation happening at the same time.",
  "mediation": "The veil is an editing system, not a disappearance. The third movement begins where the body and the rule meet a surface that can interrupt both. Lace, shadow, fabric, blur, flowers, hair, hands, and darkness all become interfaces. They do not simply hide the figure. They decide how slowly the figure can arrive.\n\nThe veiling route is held through iconography, Vera Icona, lace, secrecy, and the larger problem of mediated access. The key point is not that the viewer is denied. The key point is that denial becomes structure. A veil produces a special kind of attention because the eye has to work without full possession. It keeps searching, comparing edges, reading textures, and inventing continuity from fragments.\n\nArt movement history clarifies the pressure. Symbolism treats the visible world as a carrier for inward states; Surrealist image logic turns ordinary surfaces into psychic interruption. The covered eye, the soft obstruction, and the displaced face do not merely hide information. They make interpretation the subject. The viewer is asked to feel the delay between perception and certainty.\n\nThis section becomes more atmospheric, with more surface interruption and slower perception, but it still carries an argument: mediation is the place where agency and constraint become visible as tension. The body wants to appear. The rule wants to organize appearance. The veil controls the tempo of access.\n\nThe idea stays modular: surface, delay, pressure, partial access. Those repeated terms create a learning path through the atmosphere. The reader can feel the mystery without getting lost inside it. The veil does not remove meaning. It makes meaning arrive through effort.",
  "synthesis": "Sight becomes visceral when these forces remain active together. The final movement refuses to solve the body, the rule, and the veil into a clean hierarchy. Agency begins the argument, constraint disciplines it, and mediation keeps it unresolved. The image becomes powerful because no single force wins.\n\nThis is the core thesis of the book: psychological pressure does not come from clear depiction alone. It comes from calculated revelation. The viewer feels the image because the image negotiates what can be seen, how quickly it can be seen, and what remains withheld even after attention has been spent. The body is present, but not fully available. Culture is legible, but not neutral. The veil interrupts, but also teaches the eye how to continue.\n\nPsychology gives the gaze its behavioral force. Research on gaze cueing and social attention shows that eye direction affects an observer's attention and social interpretation, which is why a portrait can feel active even when nothing in the frame moves. The gaze is not only a theme. It is a human signal system.\n\nThe synthesis refuses easy balance. Large images take authority, and the argument holds sight in motion instead of pretending it has settled. The instability is not decoration. It is the final proof of the argument: unstable sight is where learning happens.\n\nThe conclusion keeps the claims careful. It does not invent quotations, publication details, or license certainty. It names the scholarly routes that support the issue and keeps the theory visible in the reading itself."
};

function mm(v) { return v + "mm"; }
function b(t, l, bot, r) { return [mm(t), mm(l), mm(bot), mm(r)]; }
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
function assetById(id) {
  for (var a = 0; a < ASSETS.length; a++) {
    if (ASSETS[a].id === id) return ASSETS[a];
  }
  return ASSETS[0];
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
  var startPage = key === "agency" ? 8 : key === "constraint" ? 17 : key === "mediation" ? 27 : 39;
  var offset = Math.max(0, n - startPage);
  var wordsPerPage = 52;
  var start = Math.min(offset * wordsPerPage, Math.max(0, words.length - wordsPerPage));
  return words.slice(start, start + wordsPerPage).join(" ");
}

function setupDoc() {
  var doc = app.documents.add();
  doc.documentPreferences.pageWidth = "210mm";
  doc.documentPreferences.pageHeight = "297mm";
  doc.documentPreferences.facingPages = true;
  doc.documentPreferences.pagesPerDocument = 50;
  doc.documentPreferences.documentBleedTopOffset = "3mm";
  doc.documentPreferences.documentBleedBottomOffset = "3mm";
  doc.documentPreferences.documentBleedInsideOrLeftOffset = "3mm";
  doc.documentPreferences.documentBleedOutsideOrRightOffset = "3mm";
  doc.marginPreferences.top = "20.790mm";
  doc.marginPreferences.bottom = "20.790mm";
  doc.marginPreferences.left = "21.000mm";
  doc.marginPreferences.right = "15.750mm";
  doc.marginPreferences.columnCount = 12;
  doc.marginPreferences.columnGutter = "5mm";
  return doc;
}

function configurePublicationPreflight(doc) {
  var profileName = "Anatomy of Looking - Color Landscape";
  var profile;
  try {
    profile = app.preflightProfiles.itemByName(profileName);
    profile.name;
  } catch (missing) {
    profile = app.preflightProfiles.itemByName("kDigPubProfileName").duplicate();
    profile.name = profileName;
  }
  profile.description = "Color landscape magazine profile. Keeps Digital Publishing checks while allowing intentional color plates and landscape orientation.";
  profile.preflightProfileRules.itemByName("ADBE_CMYPlates").flag = 1699890274;
  profile.preflightProfileRules.itemByName("ADBE_PageSizeOrientation").flag = 1699890274;
  doc.preflightOptions.preflightWorkingProfile = profile;
  doc.preflightOptions.preflightOff = false;
  return profile;
}

function addSwatch(doc, name, values) {
  try {
    var s = doc.colors.itemByName(name);
    s.name;
    return s;
  } catch (e) {
    return doc.colors.add({name: name, model: ColorModel.PROCESS, space: ColorSpace.RGB, colorValue: values});
  }
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
    rect.fillColor = page.parent.parent.colors.itemByName("Ink");
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
  try {
    app.interactivePDFExportPreferences.exportReaderSpreads = false;
    app.interactivePDFExportPreferences.generateThumbnails = true;
    doc.exportFile(ExportFormat.INTERACTIVE_PDF, pdfFile, false);
    return "interactive";
  } catch (interactiveErr) {}
  var preset = null;
  try {
    app.pdfExportPreferences.includeHyperlinks = true;
    app.pdfExportPreferences.exportLayers = false;
  } catch (prefsErr) {}
  try {
    preset = app.pdfExportPresets.itemByName("[High Quality Print]");
    preset.name;
  } catch (e) {
    preset = app.pdfExportPresets.item(0);
  }
  doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, preset);
  return "print";
}

function writeBuildReport(doc) {
  var reportFile = File(OUTPUT_REPORT);
  if (!reportFile.parent.exists) reportFile.parent.create();
  var report = {
    document: "The Anatomy of Looking",
    generatedAt: new Date().toString(),
    pageCount: doc.pages.length,
    facingPages: doc.documentPreferences.facingPages,
    trim: "A4 portrait 210mm x 297mm",
    bleed: "3mm all sides",
    columns: 12,
    assetCount: ASSETS.length,
    linkCount: doc.links.length,
    missingLinks: countMissingLinks(doc),
    hyperlinkCount: doc.hyperlinks.length,
    tocStyles: doc.tocStyles.length,
    tocBookmarks: doc.bookmarks.length,
    tocHyperlinks: doc.hyperlinks.length,
    preflightProfile: doc.preflightOptions.preflightWorkingProfile,
    intentionalColorLandscape: true,
    pdfExportMode: doc.extractLabel("pdfExportMode"),
    textFrameCount: doc.textFrames.length,
    oversetTextFrames: countOversetFrames(doc),
    moodyLayoutRules: [
      "dark ink and archival cream base",
      "muted gold and slate accents",
      "large image fields",
      "overlap captions",
      "broken text flow",
      "full-bleed pressure pages",
      "solid paper caption panels"
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
  var label = "A controlled glimpse becomes part of the argument.";
  colorPanel(page, bounds, cream, 98);
  var tf = textFrame(page, bounds, label, 6.2, "Bold", ink, 100);
  return tf;
}

function nativeTocSource(page, title, sourceStyle) {
  var source = page.textFrames.add();
  source.geometricBounds = pageBounds(page, b(2, 2, 8, 70));
  source.contents = title;
  source.paragraphs.item(0).appliedParagraphStyle = sourceStyle;
  source.nonprinting = true;
  return source;
}

function nativeAdobeToc(doc, ink, gold) {
  var sourceStyle = doc.paragraphStyles.add({name: "TOC Source Heading"});
  var entryStyle = doc.paragraphStyles.add({name: "TOC Entry"});
  var titleStyle = doc.paragraphStyles.add({name: "TOC Title"});
  try {
    entryStyle.pointSize = 11;
    entryStyle.leading = 16;
    entryStyle.spaceAfter = 10;
    entryStyle.fillColor = ink;
    entryStyle.tabStops.add({position: "150mm", alignment: TabStopAlignment.RIGHT_ALIGN});
    titleStyle.pointSize = 24;
    titleStyle.leading = 29;
    titleStyle.spaceAfter = 18;
    titleStyle.fillColor = ink;
  } catch (styleErr) {}

  nativeTocSource(doc.pages.item(4), "Opening Thesis", sourceStyle);
  nativeTocSource(doc.pages.item(7), "The Body", sourceStyle);
  nativeTocSource(doc.pages.item(16), "The Rule", sourceStyle);
  nativeTocSource(doc.pages.item(26), "The Veil", sourceStyle);
  nativeTocSource(doc.pages.item(38), "Synthesis", sourceStyle);
  nativeTocSource(doc.pages.item(47), "Sources", sourceStyle);

  var tocStyle = doc.tocStyles.add({
    name: "Magazine Contents",
    title: "CONTENTS",
    titleStyle: titleStyle,
    createBookmarks: true,
    makeAnchor: true
  });
  tocStyle.tocStyleEntries.add(sourceStyle.name, {
    formatStyle: entryStyle,
    pageNumberPosition: PageNumberPosition.AFTER_ENTRY,
    separator: "\t"
  });

  app.activeWindow.activePage = doc.pages.item(3);
  doc.createTOC(tocStyle, false, undefined, ["24mm", "28mm"], false, doc.activeLayer);
  var tocFrame = doc.pages.item(3).textFrames.lastItem();
  tocFrame.geometricBounds = pageBounds(doc.pages.item(3), b(34, 24, 242, 188));
  try {
    tocFrame.textFramePreferences.insetSpacing = ["2mm", "2mm", "2mm", "2mm"];
    tocFrame.textFramePreferences.verticalJustification = VerticalJustification.TOP_ALIGN;
  } catch (frameErr) {}
  fitText(tocFrame, 8);
}

function pageNum(page, n, ink) {
  textFrame(page, b(282, 184, 289, 202), ("0" + n).slice(-2), 6.5, "Regular", ink, 100);
}

function saveDesktopFiles(doc) {
  var inddFile = File(OUTPUT_INDD);
  var idmlFile = File(OUTPUT_IDML);
  if (!inddFile.parent.exists) inddFile.parent.create();
  doc.save(inddFile);
  doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile);
  doc.insertLabel("pdfExportMode", exportPdf(doc));
  writeBuildReport(doc);
}

function cover(page, doc, ink, cream, gold) {
  var item = assetById("A58");
  colorPanel(page, b(0, 0, 297, 210), ink, 100);
  imageFrame(page, b(30, 24, 232, 186), item, 100);
  colorPanel(page, b(236, 24, 286, 186), cream, 100);
  textFrame(page, b(240, 28, 269, 182), "THE ANATOMY\rOF LOOKING", 24, "Bold", ink, 100);
  textFrame(page, b(270, 62, 282, 148), "women, attention, and the psychology of sight", 8, "Regular", ink, 100);
}

function frontMatter(page, n, doc, ink, cream, gold) {
  if (n === 2) {
    textFrame(page, b(62, 24, 118, 170), "The Anatomy\rof Looking", 30, "Bold", ink, 100);
    textFrame(page, b(126, 26, 152, 160), "A 50-page visual psychology issue on attention, image memory, and human sight.", 10, "Regular", ink, 100);
    textFrame(page, b(245, 24, 272, 160), "Issue dossier: psychology of sight, image memory, Symbolism, Surrealist interruption, and the human habit of reading faces before words.", 7, "Regular", ink, 100);
  } else if (n === 3) {
    textFrame(page, b(216, 24, 271, 182), "CREDITS / RIGHTS NOTE\rImages are credited in the source register at the back. Adobe Stock, Unsplash, archive, and local image files require final rights confirmation before publication.", 8, "Regular", ink, 100);
  } else {}
}

function introPage(page, n, doc, ink, cream, gold) {
  imageFrame(page, b(32, 24, 132, 84), groupAsset("Mediation", n), 100);
  imageFrame(page, b(88, 98, 178, 186), groupAsset("Constraint", n), 100);
  imageFrame(page, b(154, 44, 238, 132), groupAsset("Agency", n), 85);
  colorPanel(page, b(188, 18, 252, 156), cream, 88);
  textFrame(page, b(196, 26, 224, 148), "The Anatomy of Looking", 21, "Bold", ink, 100);
  textFrame(page, b(226, 27, 258, 160), COPY.intro, 8.6, "Regular", ink, 100);
  caption(page, b(124, 72, 145, 134), groupAsset("Mediation", n), ink, cream);
}

function articlePage(page, n, section, item, doc, ink, cream, gold, slate) {
  var mode = n % 6;
  var accent = section === "MEDIATION" ? slate : gold;
  if (mode === 0) {
    imageFrame(page, b(24, 14, 216, 142), item, 100);
    colorPanel(page, b(144, 122, 205, 194), cream, 96);
    textFrame(page, b(152, 130, 176, 188), section, 18, "Bold", ink, 100);
    textFrame(page, b(176, 130, 204, 188), copyChunk(section.toLowerCase(), n), 7.8, "Regular", ink, 100);
    caption(page, b(196, 24, 216, 92), item, ink, cream);
  } else if (mode === 1) {
    imageFrame(page, b(42, 68, 210, 196), item, 100);
    colorPanel(page, b(18, 22, 240, 58), cream, 98);
    textFrame(page, b(44, 28, 198, 52), section, 18, "Bold", ink, 100);
    colorPanel(page, b(150, 46, 204, 176), cream, 96);
    textFrame(page, b(156, 52, 198, 168), copyChunk(section.toLowerCase(), n), 7.2, "Regular", ink, 100);
  } else if (mode === 2) {
    imageFrame(page, b(0, 0, 297, 210), item, 100);
    colorPanel(page, b(78, 0, 116, 210), cream, 98);
    textFrame(page, b(82, 26, 112, 182), "ONLY ONE EYE REMAINS, THE IMAGE GETS LOUDER.", 18, "Bold", ink, 100);
    colorPanel(page, b(212, 18, 278, 100), cream, 98);
    textFrame(page, b(218, 24, 272, 94), copyChunk(section.toLowerCase(), n), 7.2, "Regular", ink, 100);
  } else if (mode === 3) {
    imageFrame(page, b(34, 20, 120, 102), item, 100);
    imageFrame(page, b(112, 92, 250, 182), item, 92);
    textFrame(page, b(124, 28, 164, 128), "A body becomes legible through pressure.", 13, "Bold", ink, 100);
    textFrame(page, b(166, 28, 210, 118), copyChunk(section.toLowerCase(), n), 7.6, "Regular", ink, 100);
    caption(page, b(106, 78, 127, 148), item, ink, cream);
  } else if (mode === 4) {
    imageFrame(page, b(42, 30, 226, 180), item, 100);
    colorPanel(page, b(26, 158, 196, 206), cream, 98);
    textFrame(page, b(36, 164, 138, 200), "THE VEIL DOES NOT DISAPPEAR THE BODY.", 14, "Bold", ink, 100);
    colorPanel(page, b(68, 24, 132, 104), cream, 96);
    textFrame(page, b(74, 30, 126, 98), copyChunk(section.toLowerCase(), n), 7.0, "Regular", ink, 100);
  } else {
    imageFrame(page, b(22, 44, 266, 178), item, 100);
    colorPanel(page, b(26, 28, 58, 128), cream, 94);
    textFrame(page, b(30, 34, 54, 122), "LOOKING IS EDITED BY ACCESS.", 12, "Bold", ink, 100);
    caption(page, b(240, 120, 264, 190), item, ink, cream);
  }
}

function backMatter(page, n, doc, ink, cream, gold) {
  if (n === 50) {
    textFrame(page, b(60, 24, 108, 172), "Sight remains\runfinished.", 28, "Bold", ink, 100);
    textFrame(page, b(226, 24, 258, 172), "Every act of looking leaves a remainder: memory, attention, and the human need to interpret what the eye cannot settle.", 8, "Regular", ink, 100);
  } else {
    var head = n === 46 ? "IMAGE CREDITS" : n === 47 ? "IMAGE CREDITS CONTINUED" : n === 48 ? "SOURCE LIST" : "REFERENCES";
    textFrame(page, b(28, 24, 48, 172), head, 16, "Bold", ink, 100);
    var body = "Images are credited in the register, and rights remain to be confirmed before publication. The issue follows agency, constraint, and mediation as three linked pressures in the psychology of sight.";
    textFrame(page, b(64, 24, 246, 172), body, 8.5, "Regular", ink, 100);
  }
}

var doc = setupDoc();
configurePublicationPreflight(doc);
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
  if (n !== 4) pageNum(page, n, ink);
}

nativeAdobeToc(doc, ink, gold);

// Final overset guard.
for (var i = 0; i < doc.textFrames.length; i++) {
  if (doc.textFrames[i].overflows) fitText(doc.textFrames[i], 6.5);
}

saveDesktopFiles(doc);
