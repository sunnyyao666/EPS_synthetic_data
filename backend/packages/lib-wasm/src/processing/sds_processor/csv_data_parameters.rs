use super::{header_names::HeaderNames, MultiValueColumns};
use serde::{Deserialize, Serialize};
use wasm_bindgen::{prelude::wasm_bindgen, JsValue};

use crate::utils::js::{from_js_value, JsCsvDataParameters};

#[derive(Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
#[wasm_bindgen]
pub struct WasmCsvDataParameters {
    pub(crate) delimiter: char,
    pub(crate) subject_id: Option<String>,
    pub(crate) use_columns: HeaderNames,
    pub(crate) multi_value_columns: MultiValueColumns,
    pub(crate) sensitive_zeros: HeaderNames,
    pub(crate) record_limit: usize,
}

impl TryFrom<JsCsvDataParameters> for WasmCsvDataParameters {
    type Error = JsValue;

    fn try_from(js_csv_data_params: JsCsvDataParameters) -> Result<Self, Self::Error> {
        from_js_value(&js_csv_data_params).map_err(|err| JsValue::from(err.to_string()))
    }
}
