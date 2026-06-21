# FindER API Specification

## Auth
* `POST /api/v1/auth/register` - Create user
* `POST /api/v1/auth/login` - Get JWT
* `POST /api/v1/auth/refresh` - Refresh JWT

## Emergencies (SOS & NLP)
* `POST /api/v1/emergencies/sos` - Trigger SOS (Anonymous supported)
* `POST /api/v1/emergencies/nlp-audio` - Upload audio for scream/fall detection
* `GET /api/v1/emergencies/active` - Get active emergencies (Dashboard)

## Resources & Routing
* `GET /api/v1/resources` - List all resources
* `POST /api/v1/resources/dispatch` - Assign resource to emergency
* `GET /api/v1/routing/best-hospital` - Get nearest hospital with bed capacity

## Hospitals (Pre-Surge)
* `GET /api/v1/hospitals/status` - Current bed availability
* `PUT /api/v1/hospitals/{id}/capacity` - Update beds
* `POST /api/v1/hospitals/{id}/surge-alert` - Incoming mass casualty warning

## Responders
* `POST /api/v1/responders/telemetry` - Update location & fatigue metrics
* `GET /api/v1/responders/fatigue-status` - Monitor responder health

## Bystanders
* `GET /api/v1/bystander/instructions/{type}` - Get offline-capable CPR/Trauma steps
