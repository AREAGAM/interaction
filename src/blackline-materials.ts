import * as THREE from "three";
export function blacklineMaterial(material: THREE.MeshPhysicalMaterial, name: string, array = false) {
  material.envMapIntensity = .72;
  material.emissive?.set("#000000");
  material.emissiveIntensity = 0;
  const steel = (color: string, roughness: number, metalness = .85) => {
    material.color.set(color); material.roughness = roughness;
    material.metalness = metalness; material.transmission = 0;
  };
  switch (name) {
    case "Frosted_Polymer":
      // Restore the light edition's dielectric cover: dark albedo tints even
      // fully transmitted light, so a dark glass base obscured the internals.
      material.color.set("#fffdfa");
      material.metalness = 0;
      material.transmission = array ? .78 : .9;
      material.thickness = .12;
      material.roughness = array ? .28 : .21;
      material.ior = 1.46;
      material.attenuationColor.set("#f2f5f3");
      material.attenuationDistance = 4;
      material.envMapIntensity = .6;
      material.clearcoat = array ? .3 : .1;
      material.clearcoatRoughness = .25;
      material.transparent = false;
      material.opacity = 1;
      break;
    case "Ivory_Edges": steel(array ? "#78847a" : "#d3ddd5", .14, .96); break;
    case "Titanium_Fasteners": steel("#ccd4cf", .19, .98); break;
    case "Internal_Ceramic":
      steel("#68736c", .44, .3);
      material.envMapIntensity = 1.05;
      material.emissive.set("#b5c3bb"); material.emissiveIntensity = .045;
      break;
    case "Optical_Diffuser":
      steel(array ? "#020503" : "#48554c", .44, .32);
      material.envMapIntensity = array ? .72 : 1.05;
      if (!array) { material.emissive.set("#b5c3bb"); material.emissiveIntensity = .025; }
      break;
    case "Subsurface_Optics":
      steel("#a4aea8", .28, .65); material.envMapIntensity = 1.25;
      material.emissive.set("#c0cdc5"); material.emissiveIntensity = .035;
      break;
    case "Optical_Edges": steel("#c8d1cc", .24, .75); material.envMapIntensity = 1.15; break;
    case "Printed_Label": steel("#020603", .65, .08); break;
    case "Champagne_Index":
      steel("#b6ff00", .22, .18);
      material.emissive.set("#99ff00"); material.emissiveIntensity = array ? .22 : .4;
      break;
    case "Amber_Lightguide":
      steel("#b6ff00", .18, .1);
      material.emissive.set("#9dff00"); material.emissiveIntensity = .7;
      break;
    default: steel("#26382a", .36, .68);
  }
}
