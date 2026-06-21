// The Visceral Theory of Sight - full 50-page InDesign layout builder
// Run from InDesign: File > Scripts > Other Script...
// Builds US Letter landscape facing pages, 3.175mm bleed, full-bleed section title pages with descriptions, multi-image spreads, captions, PDF, and audit report.

var ASSETS = [
  {
    "id": "A01",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-01.jpg",
    "title": "a01-mediation-a-photograph-of-an-attractive-woman-with-a-w",
    "group": "Group 3: Mediation",
    "caption": "The flowers soften the restraint, but do not remove its force.",
    "short_caption": "Beauty becomes the blindfold\u2019s alibi."
  },
  {
    "id": "A02",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-02.jpg",
    "title": "a06-social-constraint-adobestock-1040196803",
    "group": "Group 2: Social Constraint",
    "caption": "The flowers bloom exactly where recognition should happen.",
    "short_caption": "Beauty replaces sight."
  },
  {
    "id": "A03",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-03.jpg",
    "title": "a07-social-constraint-adobestock-1044937382",
    "group": "Group 2: Social Constraint",
    "caption": "The white stroke silences the gaze with surgical calm.",
    "short_caption": "The eye is edited out."
  },
  {
    "id": "A04",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-04.jpg",
    "title": "a08-social-constraint-adobestock-1225023891",
    "group": "Group 2: Social Constraint",
    "caption": "Her face becomes a garden, but the flowers still perform the work of concealment.",
    "short_caption": "Bloom as blindfold."
  },
  {
    "id": "A05",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-05.jpg",
    "title": "a09-social-constraint-adobestock-140076283",
    "group": "Group 2: Social Constraint",
    "caption": "The hands do not fully hide her. They make the act of hiding visible.",
    "short_caption": "Defense becomes gesture."
  },
  {
    "id": "A06",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-06.jpg",
    "title": "a10-social-constraint-adobestock-1462135790",
    "group": "Group 2: Social Constraint",
    "caption": "Gold catches the light while the face withdraws into shadow.",
    "short_caption": "Adornment becomes armor."
  },
  {
    "id": "A07",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-07.jpg",
    "title": "a11-social-constraint-adobestock-206067082",
    "group": "Group 2: Social Constraint",
    "caption": "She covers her sight, then paints another gaze over the absence.",
    "short_caption": "A false eye performs the feeling."
  },
  {
    "id": "A08",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-08.jpg",
    "title": "a12-social-constraint-adobestock-268225510",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A09",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-09.jpg",
    "title": "a13-social-constraint-adobestock-320500758",
    "group": "Group 2: Social Constraint",
    "caption": "The veil does not block the gaze; it makes looking feel forbidden.",
    "short_caption": "Lace turns vision into trespass."
  },
  {
    "id": "A10",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-10.jpg",
    "title": "a14-social-constraint-adobestock-368079012",
    "group": "Group 2: Social Constraint",
    "caption": "One eye meets us through the flower\u2019s shadow, half invitation, half defense.",
    "short_caption": "Nature becomes a mask."
  },
  {
    "id": "A11",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-11.jpg",
    "title": "a15-social-constraint-adobestock-378198491",
    "group": "Group 2: Social Constraint",
    "caption": "The blue fabric does not conceal her completely; it makes her appear underwater, suspended between access and refusal.",
    "short_caption": "Visibility dissolves into blue."
  },
  {
    "id": "A12",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-12.jpg",
    "title": "a16-social-constraint-adobestock-565582008",
    "group": "Group 2: Social Constraint",
    "caption": "The face breaks apart, but the eyes remain \u2014 watchful, multiplied, impossible to silence.",
    "short_caption": "Fragments still look back."
  },
  {
    "id": "A13",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-13.jpg",
    "title": "a17-social-constraint-adobestock-720156971",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A14",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-14.jpg",
    "title": "a18-social-constraint-adobestock-730927617",
    "group": "Group 2: Social Constraint",
    "caption": "The repeated faces turn the gaze into public noise: many eyes, no single witness.",
    "short_caption": "The gaze becomes a crowd."
  },
  {
    "id": "A15",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-15.jpg",
    "title": "a19-social-constraint-adobestock-973721353",
    "group": "Group 2: Social Constraint",
    "caption": "Clouds and trees cross the face like a second memory, replacing sight with interior weather.",
    "short_caption": "The mind becomes the landscape."
  },
  {
    "id": "A16",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-16.jpg",
    "title": "a20-mediation-alex-bracken-l1sjo7tmvec-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The veil softens the mouth and fractures the gaze into texture.",
    "short_caption": "The face becomes fabric."
  },
  {
    "id": "A17",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-17.jpg",
    "title": "a21-raw-agency-alexander-krivitskiy-az7rqwlwkhi-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A18",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-18.jpg",
    "title": "a22-social-constraint-alexander-krivitskiy-gfopukdkmvo-uns",
    "group": "Group 1: Raw Agency",
    "caption": "The eye remains visible through the lace, making the act of looking feel intimate and forbidden.",
    "short_caption": "Lace makes looking trespass."
  },
  {
    "id": "A19",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-19.jpg",
    "title": "a23-mediation-allef-vinicius-dkrntf-jgtw-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "Leaves interrupt the portrait gently, as if nature itself has chosen what may be seen.",
    "short_caption": "The gaze hides in green."
  },
  {
    "id": "A20",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-20.jpg",
    "title": "a24-raw-agency-amir-geshani-2jh8d3chnec-unsplash",
    "group": "Group 3: Mediation",
    "caption": "She holds the obstruction herself, turning concealment into control.",
    "short_caption": "She edits the view."
  },
  {
    "id": "A21",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-21.jpg",
    "title": "a25-social-constraint-andrey-zvyagintsev-t8iknlqojcq-unspl",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A22",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-22.jpg",
    "title": "a26-mediation-arielle-allouche-h82rqe4gria-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A23",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-23.jpg",
    "title": "a27-raw-agency-baran-lotfollahi-lobgof8rurg-unsplash",
    "group": "Group 3: Mediation",
    "caption": "The closed eye turns the image inward; the fabric makes silence feel physical.",
    "short_caption": "Sight folds into silence."
  },
  {
    "id": "A24",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-24.jpg",
    "title": "a28-social-constraint-birmingham-museums-trust-oqpbewogd0o",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A25",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-25.jpg",
    "title": "a29-mediation-boston-public-library-grbfmxpumu4-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A26",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-26.jpg",
    "title": "a30-raw-agency-brunxs-monochrome-spniqdcpi9u-unsplash",
    "group": "Group 3: Mediation",
    "caption": "The shadows do not cover her completely; they divide the gaze into risk and revelation.",
    "short_caption": "One eye survives the dark."
  },
  {
    "id": "A27",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-27.jpg",
    "title": "a31-social-constraint-caleb-kastein-lmnz6-icim8-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "The eye survives the dark, but the rest of the face slips out of reach.",
    "short_caption": "One eye holds the room."
  },
  {
    "id": "A28",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-28.jpg",
    "title": "a32-mediation-camila-quintero-franco-mc852jack1g-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A29",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-29.jpg",
    "title": "a33-raw-agency-carl-cheng-o4l-vetcxhy-unsplash",
    "group": "Group 3: Mediation",
    "caption": "The covered lenses turn sight into repair, damage, and evidence.",
    "short_caption": "Vision becomes patched evidence."
  },
  {
    "id": "A30",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-30.jpg",
    "title": "a34-social-constraint-cole-keister-d6zqt8nfiq4-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "The foil frames the gaze like something precious, trapped, and half-protected.",
    "short_caption": "The gaze cuts through gold."
  },
  {
    "id": "A31",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-31.jpg",
    "title": "a35-mediation-darius-bashar-3xegkkbinck-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The face moves faster than recognition, leaving the eye as the only anchor.",
    "short_caption": "Identity slips; the eye remains."
  },
  {
    "id": "A32",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-32.jpg",
    "title": "a36-raw-agency-drew-dizzy-graham-ctkgzjtmjqu-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A33",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-33.jpg",
    "title": "a37-social-constraint-elias-maurer-ssplu7ipc8g-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Text covers the face, but the eye reads back through the surface.",
    "short_caption": "The archive looks back."
  },
  {
    "id": "A34",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-34.jpg",
    "title": "a38-mediation-elvis-kaiser-rqbk5ez6qa0-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A35",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-35.jpg",
    "title": "a39-raw-agency-enesh-taganova-ioxgidqvqyq-unsplash-1",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A36",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-36.jpg",
    "title": "a40-social-constraint-erik-mclean-gjtz5ckgeew-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "The darkness does not hide the gaze; it sharpens its accusation.",
    "short_caption": "The eye becomes evidence."
  },
  {
    "id": "A37",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-37.jpg",
    "title": "a41-mediation-europeana-lbt8newonko-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A38",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-38.jpg",
    "title": "a42-raw-agency-europeana-wwghncxmcqi-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A39",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-39.jpg",
    "title": "a43-social-constraint-evilicio-inc-1hty8zlswls-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A40",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-40.jpg",
    "title": "a44-mediation-flaviu-costin-vr-sbbcwklc-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The cloth protects and confines at once, leaving one eye to carry the whole portrait.",
    "short_caption": "One opening, one witness."
  },
  {
    "id": "A41",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-41.jpg",
    "title": "a45-raw-agency-good-faces-r8vsytyy2oe-unsplash",
    "group": "Group 3: Mediation",
    "caption": "The face dissolves into motion, as if memory cannot hold it still.",
    "short_caption": "Recognition loses focus."
  },
  {
    "id": "A42",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-42.jpg",
    "title": "a46-social-constraint-harry-quan-g1iycecw2ei-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A43",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-43.jpg",
    "title": "a47-mediation-igor-rand-giw9ccl3hxa-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A44",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-44.jpg",
    "title": "a48-raw-agency-ilya-mondryk-oceeo0ayn1s-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A45",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-45.jpg",
    "title": "a49-social-constraint-janko-ferlic-brzt6bdt6na-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A46",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-46.jpg",
    "title": "a50-mediation-jr-korpa-0lokelbdsbw-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The face appears twice, but neither version offers certainty.",
    "short_caption": "Doubling does not reveal."
  },
  {
    "id": "A47",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-47.jpg",
    "title": "a51-raw-agency-library-of-congress-v0jinhbf3xq-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A48",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-48.jpg",
    "title": "a52-social-constraint-lorraine-hill-4dyxkga2gxa-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "The eye peers through a torn aperture, caught between protection and surveillance.",
    "short_caption": "A small hole becomes a gaze."
  },
  {
    "id": "A49",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-49.jpg",
    "title": "a53-mediation-mahdi-bafande-rw-azxeky7q-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "Light cuts across the eye like a wound; the rest of the face falls silent.",
    "short_caption": "Light becomes incision."
  },
  {
    "id": "A50",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-50.jpg",
    "title": "a54-raw-agency-nastia-petruk-f-hajyv3wye-unsplash",
    "group": "Group 3: Mediation",
    "caption": "The leaves interrupt the portrait softly, but the gaze remains direct and unhidden.",
    "short_caption": "Nature edits the face."
  },
  {
    "id": "A51",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-51.jpg",
    "title": "a55-social-constraint-nina-zeynep-guler-fjjivsx-bxm-unspla",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A52",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-52.jpg",
    "title": "a56-mediation-noah-buscher-11ldehfy-ha-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "Play becomes obstruction; sweetness performs the work of concealment.",
    "short_caption": "Candy becomes a mask."
  },
  {
    "id": "A53",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-53.jpg",
    "title": "a57-raw-agency-ovie-ogege-6bwt4ci-ujs-unsplash",
    "group": "Group 3: Mediation",
    "caption": "The glasses split the face into surface and shadow, making style feel like defense.",
    "short_caption": "Coolness becomes cover."
  },
  {
    "id": "A54",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-54.jpg",
    "title": "a58-social-constraint-see-plus-np3s9byoqac-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A55",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-55.jpg",
    "title": "a59-mediation-smithsonian-elpq3w9epnk-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A56",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-56.jpg",
    "title": "a60-raw-agency-smithsonian-otg-zz0tybe-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A57",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-57.jpg",
    "title": "a61-social-constraint-teslariu-mihai-tk-szddiuis-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  },
  {
    "id": "A58",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-58.jpg",
    "title": "a62-mediation-the-new-york-public-library-ndjv4ntdf6g-unsp",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A59",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-59.jpg",
    "title": "a63-raw-agency-toa-heftiba-fv1lunshcaw-unsplash",
    "group": "Group 3: Mediation",
    "caption": "A surface intervenes, and sight has to earn the face.",
    "short_caption": "A surface intervenes, and sight has to earn the face."
  },
  {
    "id": "A60",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-60.jpg",
    "title": "a64-social-constraint-umanoide-xjp9ak1oqhw-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "False eyes replace the real ones, turning the portrait into a performance of seeing.",
    "short_caption": "The mask learns to look."
  },
  {
    "id": "A61",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-61.jpg",
    "title": "a65-mediation-umesh-soni-hpklbuuel-k-unsplash",
    "group": "Group 2: Social Constraint",
    "caption": "The pose turns looking into a rule already agreed to.",
    "short_caption": "The pose turns looking into a rule already agreed to."
  },
  {
    "id": "A62",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-62.jpg",
    "title": "a66-mediation-woman-obscured-by-white-flowers-creating-a-d",
    "group": "Group 3: Mediation",
    "caption": "The flowers are gentle, but their placement is absolute: beauty refuses access.",
    "short_caption": "Softness blocks the gaze."
  },
  {
    "id": "A63",
    "path": "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/assets/asset-63.jpg",
    "title": "a67-social-constraint-zachary-kadolph-qbjgfnctwbu-unsplash",
    "group": "Group 1: Raw Agency",
    "caption": "Presence arrives before permission; the body speaks first.",
    "short_caption": "Presence arrives before permission; the body speaks first."
  }
];
var OUTPUT_INDD = "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.indd";
var OUTPUT_IDML = "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.idml";
var OUTPUT_PDF = "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/output/pdf/the-visceral-theory-of-sight-50pp-indesign-auto.pdf";
var OUTPUT_REPORT = "/home/ubuntu/repos/theory-of-sigh/visceral-production-route/reports/indesign-full-layout-auto-report.json";

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

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

var COVER_PATH = "/home/ubuntu/repos/theory-of-sigh/images/cover.jpg";

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
      "dark ink and archival cream base",
      "muted gold and slate accents",
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
    textFrame(page, b(40, 18, 96, 230), "Sight remains\runfinished.", 34, "Bold", cream, 100);
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
    textFrame(page, b(40, 18, 200, 255), "The Visceral Theory of Sight is a visual-psychology issue on gaze, image memory, and the veil. Photographs are credited in the Image Source Register; scholarly works are listed under Works Consulted. Set in Helvetica and Times, printed white on black.", 10, "Regular", cream, 100);
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
