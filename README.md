# panketaler-wasserampel
Home Assistant Integration für die Wasserampel der Gemeinde Panketal

# Panketaler Wasserampel für Home Assistant

Diese Integration für Home Assistant zeigt den aktuellen Status der Wasserampel der Gemeinde Panketal an.

## Installation

### Manuelle Installation

1. Kopiere den Ordner `custom_components/panketaler_wasserampel` in dein Home Assistant Verzeichnis `/config/custom_components/`
2. Starte Home Assistant neu
3. Füge die Integration über die Konfiguration > Integrationen oder über die YAML-Konfiguration hinzu

### YAML Konfiguration

```yaml
sensor:
  - platform: panketaler_wasserampel
    name: Panketaler Wasserampel
    url: http://www.eigenbetrieb-panketal.de/wassersparen/
```

## Features

- Zeigt den aktuellen Status der Wasserampel an (grün, gelb, rot)
- Bietet einen numerischen Sensor (1=grün, 2=gelb, 3=rot) für Automatisierungen

## Automatisierungsbeispiel

```yaml
automation:
  - alias: "Benachrichtigung bei Wassersperre"
    trigger:
      - platform: state
        entity_id: sensor.panketaler_wasserampel_numerisch
        to: "3"
    action:
      - service: notify.mobile_app
        data:
          title: "Achtung: Wasserampel auf ROT!"
          message: "Die Wasserampel Panketal steht auf ROT. Wassernutzung im Außenbereich verboten!"
```

## Autor

Gunnar Neuendorf (@morbeth)
