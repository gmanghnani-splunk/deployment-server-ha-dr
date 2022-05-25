import{_ as e,a as i}from"./_rollupPluginBabelHelpers-deef47fd.js";import{a as l,t as s,u as n,$ as t}from"./vendor-e1fcc605.js";import{g as a}from"./GlobalConfigUtil-2d540963.js";var r={aws_config:{label:"SQS Configuration",fields:[{label:"Region",field:"aws_region"},{label:"SQS Queue",field:"sqs_queue"}]},aws_config_rule:{label:"Rules Configuration",accountField:"account",fields:[{label:"Region",field:"region"},{label:"Config Rules",field:"rule_names"}]},splunk_ta_aws_sqs:{label:"SQS Configuration",fields:[{label:"Region",field:"aws_region"},{label:"SQS Queues",field:"sqs_queues"}]}},o='\x3c!--htmlhint spec-char-escape:false, id-class-value:false --\x3e\n<!DOCTYPE html>\n\x3c!--\n-- SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>\n-- SPDX-License-Identifier: LicenseRef-Splunk-8-2021\n--\n--\x3e\n\n<dt class="<%- dtClassName %> custom-term" style="width: 250px;"><%- name %></dt>\n<dd class="<%- ddClassName %> custom-description" style="margin-left: 250px;"><%- value %></dd>',u=function(){function u(e,s,n,t){i(this,u),this.globalConfig=e,this.serviceName=s,this.el=n,this.row=t,this.entities=a(e,s).entity,this.groupFields=this.serviceName in r?r[this.serviceName].fields:[],this.IGNORE_FIELDS=["metric_dimensions","metric_names","statistics"].concat(l(this.groupFields,"field"))}return e(u,[{key:"render",value:function(e){var i=this;this.el.innerHTML=s('<!DOCTYPE html>\n\x3c!--\n-- SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>\n-- SPDX-License-Identifier: LicenseRef-Splunk-8-2021\n--\n--\x3e\n\n<td colspan="9">\n    <dl class="custom-definition-list">\n    </dl>\n</td>\n')();var a="",r=this.entities.map((function(e){return e.field}));if(a=Object.keys(e).filter((function(e){return r.indexOf(e)>-1&&-1===i.IGNORE_FIELDS.indexOf(e)})).map((function(e){return i.entities.find((function(i){return i.field===e}))})).filter((function(e){return!("options"in e&&"display"in e.options&&!1===e.options.display||null===e.label||""===e.label)})).sort((function(e,i){return e.label>i.label?1:e.label<i.label?-1:0})).map((function(i){var l=e[i.field]||"N/A";if("metric_namespace"===i.field)try{l=JSON.parse(l),l=n(l).join(", ")}catch(e){}return l.length>100&&(l=l.substring(0,100),l+="..."),s(o)({dtClassName:"custom-term-ellipsis",ddClassName:"",name:i.label,value:l})})).join(""),this.groupFields.length>0){a+=s(o)({dtClassName:"custom-label",ddClassName:"custom-label",name:"Region",value:this.groupFields[1].label});for(var u=-1,d=l(this.groupFields,"field").map((function(i){var l=JSON.parse(e[i]||"[]");if(-1===u)u=l.length;else if(l.length!==u)throw new Error("Wrong group");return l})),f=0;f<u;f++){var c=d[0][f],m=d[1][f];m||(m="ALL"),a+=s(o)({dtClassName:"custom-detail-field",ddClassName:"custom-detail-field",name:c,value:m})}}return t(".custom-definition-list").html(a),this}}]),u}();export{u as default};
//# sourceMappingURL=CustomInputRow.js.map
