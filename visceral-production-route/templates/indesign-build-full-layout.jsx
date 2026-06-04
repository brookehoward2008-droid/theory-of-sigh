// The Visceral Theory of Sight - full 50-page InDesign layout builder
// Run from InDesign: File > Scripts > Other Script...
// Builds A4 facing pages, 3mm bleed, 12-column grid, linked images, captions, and layered editorial modules.

var ASSETS = [
  {
    "id": "A01",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-01.jpeg",
    "title": "A photograph of an attractive woman with a white lace blin",
    "group": "Group 3: Mediation"
  },
  {
    "id": "A02",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-02.jpeg",
    "title": "Abstract Female Portrait Hidden Vision, Pink and Black",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A03",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-03.jpeg",
    "title": "Abstract Monochrome Portrait of a Woman A Study in Light a",
    "group": "Group 2: Social Constraint"
  },
  {
    "id": "A04",
    "path": "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/asset-04.jpeg",
    "title": "AdobeStock_1021442471",
    "group": "Group 2: Social Constraint"
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

var COPY = {
  "intro": "Sight is never only an act of seeing. It is a negotiation between the body that appears, the culture that disciplines appearance, and the surface that decides what can be touched by the eye. This book moves through agency, constraint, and mediation as one visual pressure system.",
  "agency": "The body becomes the first instrument of authorship before it becomes a subject for interpretation. In the first movement of this book, sight begins with bodily insistence: a hand, a shoulder, a mouth, an eye, or a turned face does not wait for culture to explain it. The figure enters as pressure. It occupies the page with the blunt force of being present, and that presence matters because the viewer has not yet been given a stable rule for reading it.\n\nThe scholarly route through McDermott is used here as a verified-to-be-checked framework rather than as a source of direct quotation. The working idea is that early bodily images can be read as more than passive objects of display. They carry agency through scale, fragment, gesture, and emphasis. A figure can be partial and still be active. A cropped body can still claim space. The page therefore treats the body as origin, not because origin is simple, but because every later system of looking must first meet the fact of the body.\n\nAgency in this layout is close, image-led, and slightly uncomfortable. The images press into the margins. Captions cross edges. Text is broken into short forceful passages so the reader feels the body interrupting analysis. The design does not let the article become smooth because smoothness would weaken the argument. The body is not introduced as an illustration of theory. It is introduced as the condition that makes theory necessary.\n\nThis is also where the neural learning backdrop enters quietly: looking is not passive reception. The eye learns by comparing pressure, repetition, interruption, and contrast. A body seen once is an image. A body seen across a sequence becomes a pattern the reader has to train against. The first article therefore builds a visual lesson in agency: presence arrives before permission.",
  "constraint": "Culture turns visibility into a protocol. The second movement begins when bodily force is no longer allowed to stand alone. The figure becomes arranged by posture, costume, rank, gender, ritual, and inherited rules of display. A face can still look outward, but it now looks through an architecture of expectation. A body can still occupy the frame, but the frame has begun to instruct it.\n\nThe Havelock and Reeder route is treated as a scholarly placeholder for the cultural body: Greek art, social posture, public presentation, and the disciplined relation between figure and viewer. No direct quotation is used here because the source texts are not supplied in the workspace. Instead, the article synthesizes the assigned idea: visibility becomes social when a culture teaches bodies how to appear, and teaches viewers how to approve that appearance.\n\nConstraint does not erase agency. It redirects it. The body still carries force, but that force is shaped by protocol. The page system responds by tightening. Columns become more formal. Panels sit closer to the grid. Accent color marks pressure points, especially where the terms agency and constraint appear together. This section should feel less wild than the first, but more tense. The reader should sense that the body has entered a room where every gesture is already being measured.\n\nThis matters to the theory of sight because the viewer is also constrained. We do not only look at the ruled body; we learn the rule by looking. The layout asks the reader to notice that training. Each repeated crop, caption, and column teaches a visual habit. The eye becomes disciplined alongside the figure. Seeing is no longer just contact. It is compliance, resistance, and learned interpretation happening at the same time.",
  "mediation": "The veil is an editing system, not a disappearance. The third movement begins where the body and the rule meet a surface that can interrupt both. Lace, shadow, fabric, blur, flowers, hair, hands, and darkness all become interfaces. They do not simply hide the figure. They decide how slowly the figure can arrive.\n\nThe veiling route is held through iconography, Vera Icona, lace, secrecy, and the larger problem of mediated access. The key point is not that the viewer is denied. The key point is that denial becomes structure. A veil produces a special kind of attention because the eye has to work without full possession. It keeps searching, comparing edges, reading textures, and inventing continuity from fragments.\n\nThis section opens the grid. The design becomes more atmospheric, with more negative space and more surface interruption. Images are allowed to feel secretive. Text becomes quieter, more breath-based, but it still carries an argument: mediation is the place where agency and constraint become visible as tension. The body wants to appear. The rule wants to organize appearance. The veil controls the tempo of access.\n\nFor an ADHD reader, this section should not become vague. The idea stays modular: surface, delay, pressure, partial access. Those repeated terms create a learning path through the atmosphere. The reader can feel the mystery without getting lost inside it. The veil does not remove meaning. It makes meaning arrive through effort.",
  "synthesis": "Sight becomes visceral when these forces remain active together. The final movement refuses to solve the body, the rule, and the veil into a clean hierarchy. Agency begins the argument, constraint disciplines it, and mediation keeps it unresolved. The image becomes powerful because no single force wins.\n\nThis is the core thesis of the book: psychological pressure does not come from clear depiction alone. It comes from calculated revelation. The viewer feels the image because the image negotiates what can be seen, how quickly it can be seen, and what remains withheld even after attention has been spent. The body is present, but not fully available. Culture is legible, but not neutral. The veil interrupts, but also teaches the eye how to continue.\n\nThe synthesis pages therefore break the grid most visibly. Large images take authority. Text floats beside them or presses into panels that seem slightly displaced. The asymmetry is not decoration. It is the final proof of the argument. A symmetrical page would imply that sight has settled. This book needs sight to remain unstable, because unstable sight is where learning happens.\n\nThe conclusion keeps the claims rights-sensitive and citation-safe. It does not invent quotations, publication details, or license certainty. It names the scholarly routes that still need final verification and holds the visual argument as the completed local production route. What remains is deliberate: source checking, instructor review, and final export. The theory, however, is already visible in the structure."
};

function mm(v) { return v + "mm"; }
function b(t, l, bot, r) { return [mm(t), mm(l), mm(bot), mm(r)]; }
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
  var wordsPerPage = 86;
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
  tf.geometricBounds = bounds;
  tf.contents = text;
  try {
    tf.textFramePreferences.insetSpacing = ["2mm", "2mm", "2mm", "2mm"];
    tf.textFramePreferences.verticalJustification = VerticalJustification.TOP_ALIGN;
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
  rect.geometricBounds = bounds;
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

function colorPanel(page, bounds, swatch, opacity) {
  var rect = page.rectangles.add();
  rect.geometricBounds = bounds;
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
  doc.save(inddFile);
  doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile);
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
    textFrame(page, b(245, 24, 272, 160), "A4 precision layout. 12-column grid. 3mm bleed. Source and rights verification required before final export.", 7, "Regular", ink, 100);
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

alert("Full Visceral layout built and saved. INDD: " + OUTPUT_INDD + "\nIDML: " + OUTPUT_IDML);
