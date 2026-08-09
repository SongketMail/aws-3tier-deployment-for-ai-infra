---
layout: "default"
okf_version: "0.1"
type: "Guide"
title: "All Project Documentation"
timestamp: 2026-08-05T22:03:00Z
topics: ["aws", "cloud", "architecture", "pdf"]
permalink: "/print_all.html"
---
{% assign ordered_paths = "index.md,architecture.md,aws-adoption-roadmap.md,developer-design-mapping.md,asg-separation-of-concern.md,root-files.md,opentofu-migration.md,ami-design.md,route53.md,jumphost.md,hybrid-onprem.md,dr-options.md,postgresql-comparison.md,ragflow-langfuse.md,antigravity-skills.md,SOP-KNOWLEDGE-FIRST-DISCOVERY.md,wazuh.md,tech-stack-comparison.md,licensing-risks.md,aws-vs-self-hosted-review.md,load-test-assumptions.md,context7.md,modules/vpc.md,modules/security_groups.md,modules/waf.md,modules/alb.md,modules/asg.md,modules/rds.md,modules/standalone_ec2.md,modules/elasticache.md,modules/jumphost.md,scripts.md,cicd.md,gitlab-efs-cicd.md,costing.md" | split: "," %}

<div class="print-all-container">
  {% for path_str in ordered_paths %}
    {% for p in site.pages %}
      {% if p.path == path_str %}
        <section class="printed-page" style="page-break-after: always; break-after: page; margin-bottom: 50px;">
          <div class="printed-page-header" style="border-bottom: 3px solid var(--lab-purple); padding-bottom: 10px; margin-bottom: 30px; margin-top: 20px;">
            <div style="font-family: var(--f-mono); font-size: 0.85em; color: var(--lab-muted); text-transform: uppercase; letter-spacing: 1px;">
              {{ p.type | default: "Documentation" }}
            </div>
            <h1 style="margin: 5px 0 15px 0; font-size: 2.5em; color: var(--lab-heading); border: none; padding: 0;">
              {{ p.title }}
            </h1>
            {% if p.topics %}
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              {% for topic in p.topics %}
                <span class="badge" style="background: var(--lab-box-bg); color: var(--lab-text); border: 1px solid var(--lab-border); padding: 4px 8px; border-radius: 4px; font-family: var(--f-mono); font-size: 11px;">#{{ topic }}</span>
              {% endfor %}
            </div>
            {% endif %}
          </div>

          <div class="printed-page-body">
            {{ p.content | markdownify }}
          </div>
        </section>
      {% endif %}
    {% endfor %}
  {% endfor %}
</div>
