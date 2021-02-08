using Newtonsoft.Json;

namespace csharp.Models
{
    public class UrlInfoViewModel
    {
        [JsonProperty("url")]
        public string URL { get; set; }

        [JsonProperty("method")]
        public string Method { get; set; }

        [JsonProperty("params")]
        public string Params { get; set; }

        [JsonProperty("body")]
        public string Body { get; set; }

        [JsonProperty("desc")]
        public string Desc { get; set; }
    }
}