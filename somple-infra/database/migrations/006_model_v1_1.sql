BEGIN;

UPDATE model_versions
SET is_active = FALSE
WHERE model_name = 'somple-risk-classifier' AND is_active = TRUE;

INSERT INTO model_versions (
    model_name, version, artifact_uri, artifact_sha256,
    training_dataset_version, metrics, is_active
)
VALUES (
    'somple-risk-classifier',
    '1.1.0',
    'local://ml/artifacts/somple-risk-classifier-v1.1.0.joblib',
    '8ea7d658403aca46be7b6ef71f75fde9bd5077ed6d8ec97a847f569e960e0d67',
    'dataset-v1-reviewed',
    '{"classifier":{"accuracy":0.7667,"precision_macro":0.5057,"recall_macro":0.5223,"f1_macro":0.5116},"regressor":{"mae":8.8325,"rmse":11.9401,"r2":0.5945},"evaluation":{"method":"2-fold stratified out-of-fold evaluation","final_fit_size":180}}'::jsonb,
    TRUE
)
ON CONFLICT (model_name, version) DO UPDATE
SET artifact_uri = EXCLUDED.artifact_uri,
    artifact_sha256 = EXCLUDED.artifact_sha256,
    training_dataset_version = EXCLUDED.training_dataset_version,
    metrics = EXCLUDED.metrics,
    is_active = TRUE;

COMMIT;
